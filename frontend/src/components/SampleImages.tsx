import { Card } from './ui/card';
import { Button } from './ui/button';
import { ImageWithFallback } from './figma/ImageWithFallback';

interface SampleImage {
  url: string;
  label: string;
  description: string;
}

interface SampleImagesProps {
  onSampleSelect: (imageUrl: string) => void;
}

const sampleImages: SampleImage[] = [
  {
    url: "src/images/754788646151236.jpeg",
    label: "Sports Car",
    description: "Luxury sports car example"
  },
  {
    url: "src/images/Dirty Car Owners Find Their Cars “Vandalized” With Amazing Drawings, And Your Car May Be Next!.jpeg",
    label: "Sedan",
    description: "Classic sedan vehicle"
  },
  {
    url: "src/images/istockphoto-175195079-612x612.jpg",
    label: "SUV",
    description: "Modern SUV example"
  }
];

export function SampleImages({ onSampleSelect }: SampleImagesProps) {
  return (
    <Card className="p-6 bg-[rgba(91,103,85,1)] border-border/50">
      <h3 className="mb-4 text-white">Try Sample Images</h3>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {sampleImages.map((image, index) => (
          <div key={index} className="space-y-2">
            <div className="relative group cursor-pointer" onClick={() => onSampleSelect(image.url)}>
              <ImageWithFallback
                src={image.url}
                alt={image.label}
                className="w-full h-32 object-cover rounded-lg transition-transform group-hover:scale-105"
              />
              <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity rounded-lg flex items-center justify-center">
                <Button size="sm" className="bg-primary text-primary-foreground hover:bg-primary/90">
                  Try This Image
                </Button>
              </div>
            </div>
            <div>
              <p className="text-sm text-white">{image.label}</p>
              <p className="text-xs text-muted-foreground">{image.description}</p>
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
}