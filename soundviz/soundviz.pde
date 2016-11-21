// output
int fps = 30;
String outputFrameFile = "output/frames/frames-#####.png";
boolean captureFrames = false;

// data
String data_file = "data/still_i_rise.json";

// ui
Speech speech;
Legend legend;
Staff staff;
int legendH = 30;

// color
color bgColor = #161414;

// time
float speed = 0.1;
float startMs = 0;
float endMs = 0;
float elapsedMs = startMs;
float frameMs = (1.0/fps) * 1000;
float totalFrames = 0;
float pxPerS = 500;
float pxPerMs = pxPerS / 1000;

void setup() {
  // set the stage
  size(1280, 720);
  colorMode(RGB, 255, 255, 255, 100);
  frameRate(fps);
  smooth();
  noStroke();
  noFill();
  background(bgColor);

  // init note labels
  ArrayList<NoteLabel> noteLabels = new ArrayList<NoteLabel>();
  noteLabels.add(new NoteLabel("C", color(255, 50, 50)));
  noteLabels.add(new NoteLabel("C#", color(90, 90, 255)));
  noteLabels.add(new NoteLabel("D", color(50, 255, 50)));
  noteLabels.add(new NoteLabel("D#", color(255, 50, 255)));
  noteLabels.add(new NoteLabel("E", color(50, 255, 255)));
  noteLabels.add(new NoteLabel("F", color(255, 255, 50)));
  noteLabels.add(new NoteLabel("F#", color(175, 50, 255)));
  noteLabels.add(new NoteLabel("G", color(50, 255, 175)));
  noteLabels.add(new NoteLabel("G#", color(255, 175, 50)));
  noteLabels.add(new NoteLabel("A", color(255, 50, 175)));
  noteLabels.add(new NoteLabel("A#", color(50, 175, 255)));
  noteLabels.add(new NoteLabel("B", color(175, 255, 50)));

  // get speech data
  JSONObject data_json = loadJSONObject(data_file);
  float minFrequency = data_json.getFloat("minFrequency");
  float maxFrequency = data_json.getFloat("maxFrequency");
  float minIntensity = data_json.getFloat("minIntensity");
  float maxIntensity = data_json.getFloat("maxIntensity");
  startMs = data_json.getFloat("start") * 1000;
  if (endMs <= 0) {
    endMs = data_json.getFloat("end") * 1000;
  }
  JSONArray syllables_json = data_json.getJSONArray("data");

  // init legend
  legend = new Legend(0, height - legendH, width, legendH, noteLabels);

  // init staff
  staff = new Staff(0, 0, width, height - legendH, noteLabels, minFrequency, maxFrequency);

  // init speech
  speech = new Speech(0, 0, width, height - legendH, noteLabels, syllables_json, minFrequency, maxFrequency, minIntensity, maxIntensity, pxPerMs);

  // determine the frames
  totalFrames = endMs * 0.001 * fps;

  // noLoop();
}

void draw(){
  background(bgColor);

  speech.render(elapsedMs);

  staff.render();

  legend.render();


  // increment time
  elapsedMs += (frameMs * speed);

  // save image
  if(captureFrames) {
    saveFrame(outputFrameFile);
  }

  // check if we should exit
  if (elapsedMs > endMs) {
    saveFrame("output/frame.png");
    exit();
  }

}

void mousePressed() {
  saveFrame("output/frame.png");
  exit();
}

Note frequencyToNote(float frequency) {
  float A4 = 440;
  float C0 = A4 * pow(2, -4.75);
  float h = 12*(log(frequency/C0)/log(2));
  int octave = floor(h / 12);
  int note = floor(h % 12);
  return new Note(note, octave);
}

class Note
{
  int index, octave;

  Note(int _index, int _octave) {
    index = _index;
    octave = _octave;
  }

  int getIndex(){
    return index;
  }

  int getOctave(){
    return octave;
  }

  boolean isInStaff(){
    // not sharp, not below E2, not above F3
    return (!isSharp() && !(index < 4 && octave <= 2 || octave < 2) && !(index > 5 && octave >= 3 || octave > 3));
  }

  boolean isSharp(){
    // notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    int[] sharps = {1,3,6,8,10};
    IntList sharpList = new IntList(sharps);
    return sharpList.hasValue(index);
  }
}

class NoteLabel
{
  String label;
  color noteColor;

  NoteLabel(String _label, color _color) {
    label = _label;
    noteColor = _color;
  }

  color getColor(){
    return noteColor;
  }

  String getLabel(){
    return label;
  }
}

class Legend
{
  int textSize = 16;
  color textColor = #000000;

  int x, y, w, h;
  ArrayList<NoteLabel> notes;
  PGraphics pg;

  Legend(int _x, int _y, int _w, int _h, ArrayList<NoteLabel> _notes) {
    x = _x;
    y = _y;
    w = _w;
    h = _h;
    notes = _notes;
    pg = createGraphics(w, h);
    setupGraphics();
  }

  void setupGraphics(){
    int noteCount = notes.size();
    float noteWidth = 1.0 * w / noteCount;

    pg.beginDraw();
    pg.noStroke();
    pg.textAlign(CENTER, CENTER);
    pg.textSize(textSize);

    for(int i=0; i<notes.size(); i++){
      NoteLabel n = notes.get(i);
      pg.fill(n.getColor());
      pg.rect(i*noteWidth, 0, noteWidth, h);
      pg.fill(textColor);
      pg.text(n.getLabel(), i*noteWidth, 0, noteWidth, h);
    }

    pg.endDraw();

  }

  void render(){
    image(pg, x, y);
  }
}

class Staff
{
  color strokeColor = #666666;
  color textColor = #ffffff;
  color centerLineColor = #8d8e6c;
  int labelW = 50;

  int strokeWidth = 1;
  int x, y, w, h;
  float minFrequency, maxFrequency;
  ArrayList<NoteLabel> notes;
  PGraphics pg;

  Staff(int _x, int _y, int _w, int _h, ArrayList<NoteLabel> _notes, float _minFrequency, float _maxFrequency) {
    x = _x;
    y = _y;
    w = _w;
    h = _h;
    notes = _notes;
    minFrequency = _minFrequency;
    maxFrequency = _maxFrequency;
    pg = createGraphics(w, h);
    setupGraphics();
  }

  void setupGraphics(){
    int currentNote = -1;
    int currentOctave = -1;
    float lastLineY = -1;
    float pxPerHz = h / (maxFrequency - minFrequency);
    float currentY = 1.0 * h;

    pg.beginDraw();
    pg.textAlign(LEFT, CENTER);

    // draw label background
    pg.fill(#000000);
    pg.noStroke();
    pg.rect(0, 0, labelW, h);

    for (int f = floor(minFrequency); f <= floor(maxFrequency); f++) {
      Note n = frequencyToNote(1.0*f);
      // note change
      if (currentNote != n.getIndex()) {
        // skip first hit, skip not in staff
        // if (currentNote >= 0 && n.isInStaff()) {
        if (currentNote >= 0) {
          pg.noFill();
          pg.stroke(strokeColor);
          pg.strokeWeight(strokeWidth);
          pg.line(0, currentY, w, currentY);
          // draw label
          if (lastLineY >= 0) {
            pg.noStroke();
            pg.fill(textColor);
            pg.text(notes.get(currentNote).getLabel() + currentOctave, 10, currentY, labelW, (lastLineY-currentY));
          }
          lastLineY = currentY;
        }
        currentNote = n.getIndex();
        currentOctave = n.getOctave();
      }
      currentY -= pxPerHz;
    }

    // draw vertical line in middle
    pg.noFill();
    pg.stroke(centerLineColor);
    pg.strokeWeight(1);
    pg.line(w*0.5, 0, w*0.5, h);

    pg.endDraw();
  }

  void render(){
    image(pg, x, y);
  }
}

class Speech
{
  color strokeColor = #444444;
  color textColor = #ffffff;
  float labelH = 30;
  float frameW = 10;

  ArrayList<Syllable> syllables;
  ArrayList<NoteLabel> notes;
  int x, y, w, h;
  float minFrequency, maxFrequency, minIntensity, maxIntensity, pxPerMs, msPerFrame;
  PGraphics pg;

  Speech(int _x, int _y, int _w, int _h, ArrayList<NoteLabel> _notes, JSONArray syllables_json, float _minFrequency, float _maxFrequency, float _minIntensity, float _maxIntensity, float _pxPerMs) {
    x = _x;
    y = _y;
    w = _w;
    h = _h;
    notes = _notes;
    minFrequency = _minFrequency;
    maxFrequency = _maxFrequency;
    minIntensity = _minIntensity;
    maxIntensity = _maxIntensity;
    pxPerMs = _pxPerMs;

    msPerFrame = 1.0 * w / pxPerMs;

    syllables = new ArrayList<Syllable>();
    for (int i = 0; i < syllables_json.size(); i++) {
      JSONObject syllable_json = syllables_json.getJSONObject(i);
      syllables.add(new Syllable(syllable_json, notes, i));
    }

    pg = createGraphics(w, h);
  }

  void render(float ms) {
    float minMs = ms - msPerFrame * 0.5;
    float maxMs = ms + msPerFrame * 0.5;

    pg.beginDraw();
    pg.clear();
    pg.textAlign(CENTER, CENTER);
    pg.colorMode(RGB, 255, 255, 255, 100);

    for (Syllable s : syllables) {
      if (s.isVisible(minMs, maxMs)) {
        float sx = norm(s.getStart(), minMs, maxMs) * w;
        float sw = s.getDuration() / msPerFrame * w;
        // draw line
        pg.noFill();
        pg.stroke(strokeColor);
        pg.strokeWeight(1);
        pg.line(sx, 0, sx, h);

        // draw frames
        for (Frame f : s.getFrames()) {
          float fx = norm(f.getStart(), minMs, maxMs) * w;
          float fy = 1.0*h - norm(f.getFrequency(), minFrequency, maxFrequency) * h;
          // draw frame
          pg.noStroke();
          pg.fill(f.getColor());
          pg.ellipse(fx, fy, frameW, frameW);
        }

         // draw label
         pg.noStroke();
         pg.fill(textColor);
         pg.text(s.getText(), sx, h - labelH, sw, labelH);
      }
    }

    pg.endDraw();

    image(pg, x, y);
  }
}

class Syllable
{
  int index;
  float start_ms, end_ms;
  String text;
  ArrayList<Frame> frames;

  Syllable(JSONObject _syllable, ArrayList<NoteLabel> _notes, int _index) {
    index = _index;
    text = _syllable.getString("syllable");
    start_ms = _syllable.getFloat("start") * 1000;
    end_ms = _syllable.getFloat("end") * 1000;

    frames = new ArrayList<Frame>();
    JSONArray frames_json = _syllable.getJSONArray("frames");
    for (int i = 0; i < frames_json.size(); i++) {
      JSONArray frame = frames_json.getJSONArray(i);
      frames.add(new Frame(frame.getFloat(0), frame.getFloat(1), frame.getFloat(2), _notes, i));
    }
  }

  boolean isVisible(float ms0, float ms1) {
    return !(start_ms > ms1 || end_ms < ms0);
  }

  float getDuration(){
    return (end_ms - start_ms);
  }

  ArrayList<Frame> getFrames(){
    return frames;
  }

  float getStart(){
    return start_ms;
  }

  String getText(){
    return text;
  }

}

class Frame
{
  float minAlpha = 5;
  float maxAlpha = 100;
  int index;
  float start_ms, frequency, intensity;
  color myColor;
  Note note;

  Frame(float _start, float _frequency, float _intensity, ArrayList<NoteLabel> _notes, int _index) {
    start_ms = _start * 1000;
    frequency = _frequency;
    intensity = _intensity;
    index = _index;
    note = frequencyToNote(frequency);
    float alpha = lerp(minAlpha, maxAlpha, intensity);
    color noteColor = _notes.get(note.getIndex()).getColor();
    myColor = color(red(noteColor), green(noteColor), blue(noteColor), alpha);
  }

  color getColor(){
    return myColor;
  }

  float getFrequency(){
    return frequency;
  }

  float getStart(){
    return start_ms;
  }

}