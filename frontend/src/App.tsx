
import image_beba35a210d99cba5d24bf85dde317cbb148d5b2 from 'figma:asset/beba35a210d99cba5d24bf85dde317cbb148d5b2.png';
import { useState } from 'react';
import { Card } from './components/ui/card';
import { Button } from './components/ui/button';
import { Badge } from './components/ui/badge';
import { ImageUpload } from './components/ImageUpload';
import { ClassificationResults } from './components/ClassificationResults';
import { SampleImages } from './components/SampleImages';
import { Brain, Zap, Cpu } from 'lucide-react';
import indriveImage from 'figma:asset/06b9ca5393f42c5f6801df156038a4c878723f50.png';

interface ClassificationResult {
  label: string;
  confidence: number;
  color: string;
}

export default function App() {
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const [isClassifying, setIsClassifying] = useState(false);
  const [results, setResults] = useState<ClassificationResult[]>([]);

  // 🔹 Handle when user uploads a file
  const handleImageSelect = async (file: File) => {
    const imageUrl = URL.createObjectURL(file);
    setSelectedImage(imageUrl);
    await classifyImage(file);
  };

  // 🔹 Handle when user clicks a sample image
  const handleSampleSelect = async (imageUrl: string) => {
    setSelectedImage(imageUrl);

    // Convert sample URL → File
    const response = await fetch(imageUrl);
    const blob = await response.blob();
    const file = new File([blob], "sample.jpg", { type: blob.type });

    await classifyImage(file);
  };

  // 🔹 Send image to backend
  const classifyImage = async (file: File) => {
    setIsClassifying(true);
    setResults([]);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch("http://localhost:8000/predict/", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();

      // 🔹 Adapt backend response into frontend format
      const newResults: ClassificationResult[] = [
        {
          label: data.is_clean,
          confidence: data.is_clean_score,
          color: data.is_clean === "clean" ? "#B3FF00" : "#fb7185",
        },
        {
          label: data.is_dent,
          confidence: data.is_dent_score,
          color: data.is_dent === "no dent" ? "#B3FF00" : "#ef4444",
        },
      ];

      setResults(newResults);
    } catch (error) {
      console.error("Error classifying image:", error);
    } finally {
      setIsClassifying(false);
    }
  };

  const handleClearImage = () => {
    setSelectedImage(null);
    setResults([]);
    setIsClassifying(false);
  };

  const handleClassifyAgain = () => {
    if (selectedImage) {
      // need to re-fetch file from selectedImage URL
      fetch(selectedImage)
        .then(res => res.blob())
        .then(blob => {
          const file = new File([blob], "reclassify.jpg", { type: blob.type });
          classifyImage(file);
        });
    }
  };

  return (
    <div className="min-h-screen bg-[rgba(193,241,29,1)]">
      {/* Header */}
      <div className="border-b border-border/50 bg-[rgba(255,255,255,0.98)]">
        <div className="container mx-auto px-4 py-6 bg-[rgba(255,255,255,1)]">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-4">
              <img 
                src={image_beba35a210d99cba5d24bf85dde317cbb148d5b2} 
                alt="InDrive Logo" 
                className="h-12 w-auto"
              />
              <div className="h-8 w-px bg-border"></div>
              <div>
                <h1 className="text-[rgba(65,58,58,1)]">AI Car Condition Assessment</h1>
                <p className="text-[rgba(65,58,58,1)]">Damage and cleanliness detection powered by InDrive ML</p>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <Badge variant="secondary" className="flex items-center space-x-1 bg-primary/10 text-[rgba(40,38,36,1)] border-primary/20">
                <Cpu className="h-3 w-3" />
              </Badge>
            </div>
          </div>
          <div className="flex items-center space-x-4 bg-[rgba(65,58,58,0)]">
            <Badge variant="outline" className="flex items-center space-x-1 border-primary/30 text-[rgba(40,38,36,1)] text-[rgba(65,58,58,1)]">
              <Brain className="h-3 w-3" />
              <span className="text-[rgba(65,58,58,1)]">Deep Learning</span>
            </Badge>
            <Badge variant="outline" className="flex items-center space-x-1 border-primary/30 text-[rgba(40,38,36,1)]">
              <Zap className="h-3 w-3" />
              <span className="text-[rgba(40,38,36,1)] text-[rgba(65,58,58,1)]">Real-time Processing</span>
            </Badge>
            <Badge variant="outline" className="flex items-center space-x-1 border-primary/30 text-[rgba(40,38,36,1)]">
              <span className="text-[rgba(40,38,36,1)] text-[rgba(65,58,58,1)]">Damage & Cleanliness Detection</span>
            </Badge>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-8">
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Left Column - Upload */}
          <div className="lg:col-span-2 space-y-6">
            <Card className="p-6 bg-[rgba(95,103,85,1)] border-border/50">
              <h2 className="mb-4 text-white">Upload Car Image for Assessment</h2>
              <ImageUpload 
                onImageSelect={handleImageSelect}
                selectedImage={selectedImage}
                onClearImage={handleClearImage}
              />
              {selectedImage && (
                <div className="mt-4 flex space-x-3">
                  <Button 
                    onClick={handleClassifyAgain} 
                    disabled={isClassifying}
                    className="bg-primary text-primary-foreground hover:bg-primary/90"
                  >
                    {isClassifying ? 'Assessing...' : 'Assess Again'}
                  </Button>
                  <Button variant="outline" onClick={handleClearImage} className="border-border text-white hover:bg-accent">
                    Clear Image
                  </Button>
                </div>
              )}
            </Card>

            <SampleImages onSampleSelect={handleSampleSelect} />
          </div>

          {/* Right Column - Results */}
          <div className="space-y-6">
            <ClassificationResults results={results} isLoading={isClassifying} />

            {/* Performance Stats */}
            <Card className="p-6 bg-[rgba(90,103,85,1)] border-border/50">
              <h3 className="mb-4 text-white font-bold">Performance</h3>
              <div className="grid grid-cols-2 gap-4 text-center">
                <div>
                  <div className="text-2xl font-medium text-primary">~2.1s</div>
                  <div className="text-xs text-muted-foreground">Avg Processing Time</div>
                </div>
                <div>
                  <div className="text-2xl font-medium text-primary">99.9%</div>
                  <div className="text-xs text-muted-foreground">Uptime</div>
                </div>
              </div>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}


// import image_beba35a210d99cba5d24bf85dde317cbb148d5b2 from 'figma:asset/beba35a210d99cba5d24bf85dde317cbb148d5b2.png';
// import { useState } from 'react';
// import { Card } from './components/ui/card';
// import { Button } from './components/ui/button';
// import { Badge } from './components/ui/badge';
// import { ImageUpload } from './components/ImageUpload';
// import { ClassificationResults } from './components/ClassificationResults';
// import { SampleImages } from './components/SampleImages';
// import { Brain, Zap, Cpu } from 'lucide-react';
// import indriveImage from 'figma:asset/06b9ca5393f42c5f6801df156038a4c878723f50.png';

// interface ClassificationResult {
//   label: string;
//   confidence: number;
//   color: string;
// }

// export default function App() {
//   const [selectedImage, setSelectedImage] = useState<string | null>(null);
//   const [isClassifying, setIsClassifying] = useState(false);
//   const [results, setResults] = useState<ClassificationResult[]>([]);

//   // Mock classification results for demo purposes
//   const mockClassification = (imageUrl: string): ClassificationResult[] => {
//     // Simple hash to consistently return the same result for the same image
//     const hash = imageUrl.split('').reduce((a, b) => {
//       a = ((a << 5) - a) + b.charCodeAt(0);
//       return a & a;
//     }, 0);
    
//     const randomValue = Math.abs(hash) / Math.pow(2, 31);
    
//     const results: ClassificationResult[] = [];
    
//     // Cleanliness assessment - only show the higher confidence result
//     const cleanConfidence = 0.7 + (randomValue * 0.25); // 0.7 to 0.95
//     const dirtyConfidence = 1 - cleanConfidence;
    
//     if (cleanConfidence > dirtyConfidence) {
//       results.push({ label: "Clean", confidence: cleanConfidence, color: "#B3FF00" });
//     } else {
//       results.push({ label: "Dirty", confidence: dirtyConfidence, color: "#fb7185" });
//     }
    
//     // Damage assessment - only show the higher confidence result
//     const noDamageConfidence = 0.6 + ((randomValue * 13) % 1) * 0.35; // 0.6 to 0.95
//     const damagedConfidence = 1 - noDamageConfidence;
    
//     if (noDamageConfidence > damagedConfidence) {
//       results.push({ label: "Not Damaged", confidence: noDamageConfidence, color: "#B3FF00" });
//     } else {
//       results.push({ label: "Damaged", confidence: damagedConfidence, color: "#ef4444" });
//     }
    
//     return results;
//   };

//   const handleImageSelect = async (file: File) => {
//     const imageUrl = URL.createObjectURL(file);
//     setSelectedImage(imageUrl);
//     await classifyImage(imageUrl);
//   };

//   const handleSampleSelect = async (imageUrl: string) => {
//     setSelectedImage(imageUrl);
//     await classifyImage(imageUrl);
//   };

//   const classifyImage = async (imageUrl: string) => {
//     setIsClassifying(true);
//     setResults([]);
    
//     // Simulate API call delay
//     await new Promise(resolve => setTimeout(resolve, 2000));
    
//     const mockResults = mockClassification(imageUrl);
//     setResults(mockResults);
//     setIsClassifying(false);
//   };

//   const handleClearImage = () => {
//     setSelectedImage(null);
//     setResults([]);
//     setIsClassifying(false);
//   };

//   const handleClassifyAgain = () => {
//     if (selectedImage) {
//       classifyImage(selectedImage);
//     }
//   };

//   return (
//     <div className="min-h-screen bg-[rgba(193,241,29,1)]">
//       {/* Header */}
//       <div className="border-b border-border/50 bg-[rgba(255,255,255,0.98)]">
//         <div className="container mx-auto px-4 py-6 bg-[rgba(255,255,255,1)]">
//           <div className="flex items-center justify-between mb-4">
//             <div className="flex items-center space-x-4">
//               <img 
//                 src={image_beba35a210d99cba5d24bf85dde317cbb148d5b2} 
//                 alt="InDrive Logo" 
//                 className="h-12 w-auto"
//               />
//               <div className="h-8 w-px bg-border"></div>
//               <div>
//                 <h1 className="text-[rgba(65,58,58,1)]">AI Car Condition Assessment</h1>
//                 <p className="text-[rgba(65,58,58,1)]">Damage and cleanliness detection powered by InDrive ML</p>
//               </div>
//             </div>
//             <div className="flex items-center space-x-3">
//               <Badge variant="secondary" className="flex items-center space-x-1 bg-primary/10 text-[rgba(40,38,36,1)] border-primary/20">
//                 <Cpu className="h-3 w-3" />

//               </Badge>
//             </div>
//           </div>
//           <div className="flex items-center space-x-4 bg-[rgba(65,58,58,0)]">
//             <Badge variant="outline" className="flex items-center space-x-1 border-primary/30 text-[rgba(40,38,36,1)] text-[rgba(65,58,58,1)]">
//               <Brain className="h-3 w-3" />
//               <span className="text-[rgba(65,58,58,1)]">Deep Learning</span>
//             </Badge>
//             <Badge variant="outline" className="flex items-center space-x-1 border-primary/30 text-[rgba(40,38,36,1)]">
//               <Zap className="h-3 w-3" />
//               <span className="text-[rgba(40,38,36,1)] text-[rgba(65,58,58,1)]">Real-time Processing</span>
//             </Badge>
//             <Badge variant="outline" className="flex items-center space-x-1 border-primary/30 text-[rgba(40,38,36,1)]">
//               <span className="text-[rgba(40,38,36,1)] text-[rgba(65,58,58,1)]">Damage & Cleanliness Detection</span>
//             </Badge>
//           </div>
//         </div>
//       </div>

//       {/* Main Content */}
//       <div className="container mx-auto px-4 py-8">
//         <div className="grid lg:grid-cols-3 gap-8">
//           {/* Left Column - Upload */}
//           <div className="lg:col-span-2 space-y-6">
//             <Card className="p-6 bg-[rgba(95,103,85,1)] border-border/50">
//               <h2 className="mb-4 text-white">Upload Car Image for Assessment</h2>
//               <ImageUpload 
//                 onImageSelect={handleImageSelect}
//                 selectedImage={selectedImage}
//                 onClearImage={handleClearImage}
//               />
//               {selectedImage && (
//                 <div className="mt-4 flex space-x-3">
//                   <Button 
//                     onClick={handleClassifyAgain} 
//                     disabled={isClassifying}
//                     className="bg-primary text-primary-foreground hover:bg-primary/90"
//                   >
//                     {isClassifying ? 'Assessing...' : 'Assess Again'}
//                   </Button>
//                   <Button variant="outline" onClick={handleClearImage} className="border-border text-white hover:bg-accent">
//                     Clear Image
//                   </Button>
//                 </div>
//               )}
//             </Card>

//             <SampleImages onSampleSelect={handleSampleSelect} />
//           </div>

//           {/* Right Column - Results */}
//           <div className="space-y-6">
//             <ClassificationResults results={results} isLoading={isClassifying} />
            
//             {/* Model Info */}


//             {/* Performance Stats */}
//             <Card className="p-6 bg-[rgba(90,103,85,1)] border-border/50">
//               <h3 className="mb-4 text-white font-bold">Performance</h3>
//               <div className="grid grid-cols-2 gap-4 text-center">
//                 <div>
//                   <div className="text-2xl font-medium text-primary">~2.1s</div>
//                   <div className="text-xs text-muted-foreground">Avg Processing Time</div>
//                 </div>
//                 <div>
//                   <div className="text-2xl font-medium text-primary">99.9%</div>
//                   <div className="text-xs text-muted-foreground">Uptime</div>
//                 </div>
//               </div>
//             </Card>
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// }