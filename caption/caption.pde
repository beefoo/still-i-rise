// output
int fps = 15;
String outputFrameFile = "output/frames/frame####.png";
boolean captureFrames = true;

// data
String data_file = "../data/still_i_rise.json";
String frame_dir = "../frames";
ArrayList<Line> lines;

// color
color textColor = #ffffff;

// time
float startMs = 0;
float endMs = 0;
float elapsedMs = startMs;
float frameMs = (1.0/fps) * 1000;
float totalFrames = 0;

void setup() {
  // set the stage
  size(640, 480);
  colorMode(RGB, 255, 255, 255, 100);
  frameRate(fps);
  smooth();
  noStroke();
  noFill();
  background(#000000);

  // get lines data
  JSONObject data_json = loadJSONObject(data_file);
  JSONArray lines_json = data_json.getJSONArray("lines");
  lines = new ArrayList<Line>();

  for (int i = 0; i < lines_json.size(); i++) {
    JSONObject line_json = lines_json.getJSONObject(i);
    lines.add(new Line(line_json, i));
  }

  // determine the frames
  endMs = lines.get(lines.size()-1).getEndMs();

  // noLoop();
}

void draw(){
  background(#000000);
  textAlign(CENTER, CENTER);
  fill(textColor);
  textSize(24);
  
  // show image
  int f = max(ceil(elapsedMs / frameMs), 1);
  String filename = frame_dir + "/" + "frame" + nf(f, 4) + ".png";
  PImage img = loadImage(filename);
  image(img, 0, 0, width, height);

  for (Line l : lines) {
    if (l.isVisible(elapsedMs)) {
      // show text
      text(l.getText(), 0, height - 60, width, 60);
    }
  }


  // increment time
  elapsedMs += frameMs;

  // save image
  if(captureFrames) {
    saveFrame(outputFrameFile);
  }

  // check if we should exit
  if (elapsedMs > endMs) {
    // saveFrame("output/frame.png");
    exit();
  }

}

void mousePressed() {
  // saveFrame("output/frame.png");
  exit();
}

class Line
{
  int index;
  float start_ms, end_ms;
  String text;

  Line(JSONObject _line, int _index) {
    index = _index;
    text = _line.getString("text");
    start_ms = _line.getFloat("start") * 1000;
    end_ms = _line.getFloat("end") * 1000;
  }

  boolean isVisible(float ms) {
    return (ms >= start_ms && ms < end_ms);
  }
  
  float getEndMs(){
    return end_ms;
  }

  String getText(){
    return text;
  }

}