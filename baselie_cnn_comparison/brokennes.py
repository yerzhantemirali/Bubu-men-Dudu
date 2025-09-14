import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from PIL import Image
from glob import glob
import os
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# ----------------------------
# Device setup
# ----------------------------
device = torch.device('mps' if torch.backends.mps.is_available() else 'cuda' if torch.cuda.is_available() else 'cpu')
print("Using device:", device)

# ----------------------------
# Paths and parameters
# ----------------------------
data_dir = "dataset/целостность"
batch_size = 16
num_epochs = 10
learning_rate = 1e-3
num_classes = 2  # clean / dirty

# ----------------------------
# Dataset preparation
# ----------------------------
clean_paths = glob(os.path.join(data_dir, "небитыйджпег", "*.jpg"))
dirty_paths = glob(os.path.join(data_dir, "битыйджпег", "*.jpg"))

all_paths = clean_paths + dirty_paths
all_labels = [0]*len(clean_paths) + [1]*len(dirty_paths)

train_paths, test_paths, train_labels, test_labels = train_test_split(
    all_paths, all_labels, test_size=0.1, stratify=all_labels, random_state=42
)
train_paths, val_paths, train_labels, val_labels = train_test_split(
    train_paths, train_labels, test_size=0.1111, stratify=train_labels, random_state=42
)

print(f"Train: {len(train_paths)}, Val: {len(val_paths)}, Test: {len(test_paths)}")

# ----------------------------
# Transformations
# ----------------------------
train_transform = transforms.Compose([
    transforms.Resize((64, 64)),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
])

val_test_transform = transforms.Compose([
    transforms.Resize((64, 64)),
    transforms.ToTensor(),
    transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
])

# ----------------------------
# Custom Dataset
# ----------------------------
class CarDataset(Dataset):
    def __init__(self, paths, labels, transform=None):
        self.paths = paths
        self.labels = labels
        self.transform = transform
        
    def __len__(self):
        return len(self.paths)
    
    def __getitem__(self, idx):
        img_path = self.paths[idx]
        label = self.labels[idx]
        image = Image.open(img_path).convert("RGB")
        if self.transform:
            image = self.transform(image)
        return image, label

train_dataset = CarDataset(train_paths, train_labels, transform=train_transform)
val_dataset   = CarDataset(val_paths, val_labels, transform=val_test_transform)
test_dataset  = CarDataset(test_paths, test_labels, transform=val_test_transform)

train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
val_loader   = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
test_loader  = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

# ----------------------------
# Simple CNN Model
# ----------------------------
class SimpleCNN(nn.Module):
    def __init__(self, num_classes=2):
        super(SimpleCNN, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            
            nn.Conv2d(16, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(64*8*8, 128),
            nn.ReLU(),
            nn.Linear(128, num_classes)
        )
        
    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x

model = SimpleCNN(num_classes=num_classes).to(device)

# ----------------------------
# Loss and optimizer
# ----------------------------
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

# ----------------------------
# Training function
# ----------------------------
def train_model(model, criterion, optimizer, train_loader, val_loader, num_epochs):
    best_acc = 0.0
    train_losses, val_losses = [], []
    
    for epoch in range(num_epochs):
        print(f"Epoch {epoch+1}/{num_epochs}")
        model.train()
        running_loss, running_corrects = 0.0, 0
        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item() * inputs.size(0)
            running_corrects += torch.sum(torch.argmax(outputs,1) == labels.data)
        
        epoch_loss = running_loss / len(train_loader.dataset)
        epoch_acc  = running_corrects.double() / len(train_loader.dataset)
        train_losses.append(epoch_loss)
        
        # Validation
        model.eval()
        val_loss, val_corrects = 0.0, 0
        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                val_loss += loss.item() * inputs.size(0)
                val_corrects += torch.sum(torch.argmax(outputs,1) == labels.data)
        
        val_epoch_loss = val_loss / len(val_loader.dataset)
        val_epoch_acc  = val_corrects.double() / len(val_loader.dataset)
        val_losses.append(val_epoch_loss)
        
        print(f"Train Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}")
        print(f"Val   Loss: {val_epoch_loss:.4f} Acc: {val_epoch_acc:.4f}")
        
        if val_epoch_acc > best_acc:
            best_acc = val_epoch_acc
            best_model_wts = model.state_dict()
    
    print(f"Best Val Acc: {best_acc:.4f}")
    model.load_state_dict(best_model_wts)
    
    # Plot losses
    plt.figure(figsize=(8,4))
    plt.plot(train_losses, label='Train Loss')
    plt.plot(val_losses, label='Val Loss')
    plt.legend()
    plt.show()
    
    return model

# ----------------------------
# Train the model
# ----------------------------
model = train_model(model, criterion, optimizer, train_loader, val_loader, num_epochs)

# ----------------------------
# Evaluate on test set
# ----------------------------
model.eval()
test_corrects = 0
with torch.no_grad():
    for inputs, labels in test_loader:
        inputs, labels = inputs.to(device), labels.to(device)
        outputs = model(inputs)
        test_corrects += torch.sum(torch.argmax(outputs,1) == labels.data)

test_acc = test_corrects.double() / len(test_loader.dataset)
print(f"Test Accuracy: {test_acc:.4f}")
