"use client";

import type React from "react";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import {
  Loader2,
  Upload,
  FileText,
  CheckCircle,
  AlertCircle,
} from "lucide-react";
import { Progress } from "@/components/ui/progress";

export default function Home() {
  const [files, setFiles] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [report, setReport] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFiles(e.target.files[0]);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!files) {
      setError("Please select a document to upload");
      return;
    }

    setUploading(true);
    setError(null);

    // Create a FormData object to send file
    const formData = new FormData();
    formData.append("file", files);

    try {
      // Simulate progress for demo purposes
      const progressInterval = setInterval(() => {
        setUploadProgress((prev) => {
          if (prev >= 95) {
            clearInterval(progressInterval);
            return prev;
          }
          return prev + 5;
        });
      }, 300);

      // Replace with your actual FastAPI endpoint
      const response = await fetch("http://127.0.0.1:8000/process", {
        method: "POST",
        body: formData,
        headers: {
          Accept: "application/json",
        },
      });

      clearInterval(progressInterval);
      setUploadProgress(100);

      if (!response.ok) {
        throw new Error(`Upload failed with status: ${response.status}`);
      }

      // Get the processed report from the backend
      const data = await response.json();
      setReport(data);
      console.log(data);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "An unknown error occurred"
      );
    } finally {
      setUploading(false);
    }
  };

  const renderFileList = () => {
    if (!files) return null;

    return (
      <div className="mt-4 space-y-2">
        <h3 className="text-sm font-medium">Selected Document:</h3>
        <div className="text-sm flex items-center gap-2">
          <FileText className="h-4 w-4 text-gray-500" />
          {files.name}
        </div>
      </div>
    );
  };

  const renderReport = () => {
    if (!report) return null;

    // This is a placeholder for how the report might be displayed
    // You would customize this based on the actual structure of your report
    return <Card className="mt-8">{report.response}</Card>;
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-4 md:p-24">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>Application Document Upload</CardTitle>
          <CardDescription>
            Upload all required documents for your application
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit}>
            <div className="grid w-full items-center gap-4">
              <div className="flex flex-col space-y-1.5">
                <div className="flex flex-col items-center justify-center border-2 border-dashed border-gray-300 rounded-lg p-6 cursor-pointer hover:bg-gray-50 transition-colors">
                  <input
                    id="file-upload"
                    name="file-upload"
                    type="file"
                    className="sr-only"
                    accept=".pdf"
                    onChange={handleFileChange}
                    disabled={uploading}
                  />
                  <label
                    htmlFor="file-upload"
                    className="cursor-pointer flex flex-col items-center"
                  >
                    <Upload className="h-10 w-10 text-gray-400 mb-2" />
                    <span className="text-sm font-medium">
                      Click to upload documents
                    </span>
                    <span className="text-xs text-gray-500 mt-1">
                      PDF files only
                    </span>
                  </label>
                </div>
              </div>

              {renderFileList()}

              {error && (
                <Alert variant="destructive" className="mt-4">
                  <AlertCircle className="h-4 w-4" />
                  <AlertTitle>Error</AlertTitle>
                  <AlertDescription>{error}</AlertDescription>
                </Alert>
              )}

              {uploading && (
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-sm">Uploading documents...</span>
                    <span className="text-sm">{uploadProgress}%</span>
                  </div>
                  <Progress value={uploadProgress} className="h-2" />
                </div>
              )}
            </div>
          </form>
        </CardContent>
        <CardFooter className="flex justify-end">
          <Button
            type="submit"
            onClick={handleSubmit}
            disabled={uploading || !files}
          >
            {uploading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Processing
              </>
            ) : (
              "Upload Documents"
            )}
          </Button>
        </CardFooter>
      </Card>

      {renderReport()}
    </main>
  );
}
