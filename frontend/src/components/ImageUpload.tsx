import { useState, useCallback } from 'react';
import { Upload, X } from 'lucide-react';
import { Card } from './ui/card';
import { Button } from './ui/button';
import { useRef } from "react";


interface ImageUploadProps {
  onImageSelect: (file: File) => void;
  selectedImage: string | null;
  onClearImage: () => void;
}

export function ImageUpload({ onImageSelect, selectedImage, onClearImage }: ImageUploadProps) {
  const [isDragging, setIsDragging] = useState(false);


  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const handleButtonClick = () => {
  fileInputRef.current?.click();
};



  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      const file = files[0];
      if (file.type.startsWith('image/')) {
        onImageSelect(file);
      }
    }
  }, [onImageSelect]);

  const handleFileSelect = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      onImageSelect(file);
    }
  }, [onImageSelect]);

  if (selectedImage) {
    return (
      <Card className="relative p-4">
        <div className="relative">
          <img
            src={selectedImage}
            alt="Selected car"
            className="w-full h-64 object-cover rounded-lg"
          />
          <Button
            variant="destructive"
            size="sm"
            className="absolute top-2 right-2"
            onClick={onClearImage}
          >
            <X className="h-4 w-4" />
          </Button>
        </div>
      </Card>
    );
  }

  return (
    <Card 
      className={`p-8 border-2 border-dashed transition-colors cursor-pointer bg-muted/10 ${
        isDragging ? 'border-primary bg-primary/10' : 'border-border hover:border-primary/50'
      }`}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
    >
      <div className="flex flex-col items-center justify-center space-y-4">
        <Upload className={`h-12 w-12 ${isDragging ? 'text-primary' : 'text-muted-foreground'}`} />
        <div className="text-center">
          <p className="mb-2 text-white">Drag and drop your car image here</p>
          <p className="mb-4 text-muted-foreground">or</p>


          {/* <label htmlFor="file-upload">
            <Button 
              variant="outline" 
              className="cursor-pointer bg-primary text-primary-foreground border-primary hover:bg-primary/90"
            >
              Choose Image
            </Button>
            <input
              id="file-upload"
              type="file"
              accept="image/*"
              onChange={handleFileSelect}
              className="hidden"
            />
          </label> */}

              <label htmlFor="file-upload">
        <span className="cursor-pointer">
          {/* <Button 
            variant="outline" 
            className="bg-primary text-primary-foreground border-primary hover:bg-primary/90"
          >
            Choose Image
          </Button> */}
          <Button 
  variant="outline" 
  onClick={handleButtonClick}
  className="bg-primary text-primary-foreground border-primary hover:bg-primary/90"
>
  Choose Image
</Button>
<input
  ref={fileInputRef}
  type="file"
  accept="image/*"
  onChange={handleFileSelect}
  className="hidden"
/>
        </span>
      </label>
      <input
        id="file-upload"
        type="file"
        accept="image/*"
        onChange={handleFileSelect}
        className="hidden"
      />

        </div>
        <p className="text-muted-foreground">Supports JPG, PNG, WebP</p>
      </div>
    </Card>
  );
}