import { Card } from './ui/card';
import { Badge } from './ui/badge';
import { Progress } from './ui/progress';

interface ClassificationResult {
  label: string;
  confidence: number;
  color: string;
}

interface ClassificationResultsProps {
  results: ClassificationResult[];
  isLoading: boolean;
}

export function ClassificationResults({ results, isLoading }: ClassificationResultsProps) {
  if (isLoading) {
    return (
      <Card className="p-6 bg-[rgba(90,103,85,1)] border-border/50">
        <h3 className="mb-4 text-white font-bold">Assessment Results</h3>
        <div className="space-y-4">
          <div className="animate-pulse">
            <div className="h-4 bg-muted rounded mb-2"></div>
            <div className="h-2 bg-muted rounded"></div>
          </div>
          <div className="animate-pulse">
            <div className="h-4 bg-muted rounded mb-2"></div>
            <div className="h-2 bg-muted rounded"></div>
          </div>
          <div className="animate-pulse">
            <div className="h-4 bg-muted rounded mb-2"></div>
            <div className="h-2 bg-muted rounded"></div>
          </div>
        </div>
      </Card>
    );
  }

  if (results.length === 0) {
    return (
      <Card className="p-6 bg-[rgba(90,103,85,1)] border-border/50">
        <h3 className="mb-4 text-white font-bold">Assessment Results</h3>
        <p className="text-muted-foreground">Upload an image to see damage and cleanliness assessment</p>
      </Card>
    );
  }

  return (
    <Card className="p-6 bg-[rgba(90,103,85,1)] border-border/50">
      <h3 className="mb-4 text-white font-bold">Classification Results</h3>
      <div className="space-y-4">
        {results.map((result, index) => (
          <div key={index} className="space-y-2">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <Badge variant="outline" style={{ borderColor: result.color, color: result.color, backgroundColor: `${result.color}15` }}>
                  {result.label}
                </Badge>
                <span className="font-medium text-white">{(result.confidence * 100).toFixed(1)}%</span>
              </div>
            </div>
            <Progress 
              value={result.confidence * 100} 
              className="h-2"
              style={{ 
                '--progress-foreground': result.color
              } as React.CSSProperties}
            />
          </div>
        ))}
      </div>
    </Card>
  );
}