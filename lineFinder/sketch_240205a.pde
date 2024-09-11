PImage img;


void setup() {
  size(2000, 1200);
  float ppi = 1080/8.5;
  img = loadImage("sample_image.jpg"); // Make sure the path is correct
  image(img, 0, 0, width, height);
  loadPixels();
  noFill();
  stroke(255, 0, 0);
  
  int[] lineArr = new int[width];
  for(int i = 0; i < width; i++) 
  {
    lineArr[i] = darkestPix(i);
    if(i != 0 && abs(lineArr[i]-lineArr[i-1]) > 100)
    {
      lineArr[i] = lineArr[i-1];
    }
  }
  
  beginShape();
  for(int i = 0; i < width; i++)
  {
    vertex(i, lineArr[i]);
  }
  endShape();
  
  JSONArray jsonArray = new JSONArray();
  for(int i = 0; i < width; i++)
  {
      jsonArray.append(lineArr[i]/ppi);
  }
  saveJSONArray(jsonArray, "data.json");
  
  
}

int darkestPix(int x) {
  float minBright = 255;
  int brightIdx = -1;
  
  for(int y = 0; y < height; y++)
  {
    int idx = y*width+x;
    float b = brightness(pixels[idx]);
    if(b < minBright) {
      minBright = b;
      brightIdx = y;
    }
  }
  return brightIdx;
}
