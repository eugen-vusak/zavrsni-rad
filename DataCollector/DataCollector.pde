import processing.serial.*;
import java.io.FileWriter;
import java.util.Arrays;
import java.lang.*;
import grafica.*;
import java.awt.event.MouseWheelEvent;
import java.awt.event.MouseWheelListener;
import java.util.Map;

final int NUM_OF_TIME_STEPS = 60; 

GPlot lastGesturePlot;
GPlot newGesturePlot;

float[] xLimAutoscale;
float[] yLimAutoscale;
float[] panningReferencePoint;

GLayer xaccNew;
GLayer yaccNew;
GLayer zaccNew;
GLayer xgyNew;
GLayer ygyNew;
GLayer zgyNew;

Serial myPort;  //port on which is arduino
FileWriter outWriter = null; //fileWriter for output file

int gestureCounter = 0;
int timeStepCounter = 0;

//booleans for connection
boolean dataAhead = false; 
boolean outputAhead = false;
int data_cnt = 0;
int output_cnt = 0;

//rectangle used to output message
int messageRectangleHeight = 0;
boolean messageAvailable = false;
boolean errorHappened = false;
String outputString = "";

int dataToRead = 0;

float minY = -32768;
float maxY = 32768;

String fullData = null;
boolean dataSaved;

HashMap<Character,String> keyToGestureName = new HashMap<Character,String>();

boolean deviceReady = false;

void setup() {
  
  keyToGestureName.put('1', "UP");
  keyToGestureName.put('2', "DOWN");
  keyToGestureName.put('3', "LEFT");
  keyToGestureName.put('4', "RIGHT");
  keyToGestureName.put('5', "PULL");
  keyToGestureName.put('6', "PUSH");
  keyToGestureName.put('7', "CIRCLE CW");
  keyToGestureName.put('8', "CIRCLE CCW");
  keyToGestureName.put('9', "LOCK");
  keyToGestureName.put('0', "UNLOCK");
  keyToGestureName.put('\'', "WAVE");
  keyToGestureName.put('+', "HELLO");

  
  //size(600, 400);
  //fullScreen();
  size(800, 600);
  background(#373737);

  surface.setResizable(true);
  frameRate(240);

  newGesturePlot = new GPlot(this);

  ///////////////////////////////////////////////////////////////////////////////

  newGesturePlot.setAllFontProperties("Roboto", #FFFFFF, 14);
  newGesturePlot.setBoxLineColor(#888888);
  newGesturePlot.setBgColor(#373737);
  newGesturePlot.setBoxBgColor(#404040);

  newGesturePlot.setLineColor(#FFFFFF);
  newGesturePlot.setPointColor(#FFFFFF);
  newGesturePlot.setPointSize(4);

  newGesturePlot.setXLim(0, NUM_OF_TIME_STEPS);

  newGesturePlot.addLayer("x_acc", new GPointsArray());
  newGesturePlot.addLayer("y_acc", new GPointsArray());
  newGesturePlot.addLayer("z_acc", new GPointsArray());

  newGesturePlot.addLayer("x_gy", new GPointsArray());
  newGesturePlot.addLayer("y_gy", new GPointsArray());
  newGesturePlot.addLayer("z_gy", new GPointsArray());

  xaccNew = newGesturePlot.getLayer("x_acc");
  yaccNew = newGesturePlot.getLayer("y_acc");
  zaccNew = newGesturePlot.getLayer("z_acc");
  xgyNew = newGesturePlot.getLayer("x_gy");
  ygyNew = newGesturePlot.getLayer("y_gy");
  zgyNew = newGesturePlot.getLayer("z_gy");

  xaccNew.setLineColor(#FF0000);
  xaccNew.setPointColor(#FF0000);
  xaccNew.setPointSize(4);

  yaccNew.setLineColor(#00FF00);
  yaccNew.setPointColor(#00FF00);
  yaccNew.setPointSize(4);

  zaccNew.setLineColor(#0000FF);
  zaccNew.setPointColor(#0000FF);
  zaccNew.setPointSize(4);

  xgyNew.setLineColor(#00FFFF);
  xgyNew.setPointColor(#00FFFF);
  xgyNew.setPointSize(4);

  ygyNew.setLineColor(#FF00FF);
  ygyNew.setPointColor(#FF00FF);
  ygyNew.setPointSize(4);

  zgyNew.setLineColor(#FFFF00);
  zgyNew.setPointColor(#FFFF00);
  zgyNew.setPointSize(4);


  newGesturePlot.setTitleText("Newly recorded gesture");

  try {
    //println(Serial.list()[0]);
    String portName = Serial.list()[0];
    myPort = new Serial(this, "/dev/ttyUSB0", 115200);
    myPort.bufferUntil('\n');
    println("connected to " + portName);
    myPort.clear();
    setMessage("connected to" + portName, false);
  }
  catch(RuntimeException e) {
    e.printStackTrace();
    setMessage(e.getMessage(), true);
  }

  String fileName = "/home/euzenmendenzien/Documents/Gamayun/2.0/DataCollector/test_data.csv";
  try {
    outWriter = new FileWriter(fileName, true);
  }
  catch(IOException e) {
    setMessage("ERROR unable to open file", true);
    println("ERROR unable to open file");
    e.printStackTrace();
  }
}


void draw() {
  if (messageAvailable) {
    output_message();
  }
  
  newGesturePlot.setPos(0, messageRectangleHeight);
  try {
    newGesturePlot.setOuterDim(width, (height - messageRectangleHeight));
  }
  catch(RuntimeException e) {
    e.printStackTrace();
  }

  newGesturePlot.beginDraw();
  newGesturePlot.drawBackground();
  newGesturePlot.drawTitle();
  newGesturePlot.drawBox();
  try {
    newGesturePlot.drawLines();
    newGesturePlot.drawPoints();
  }
  catch(Exception e) {
    //println(e.getMessage());
  }
  newGesturePlot.drawXAxis();
  newGesturePlot.drawYAxis();
  newGesturePlot.endDraw();
}



void serialEvent(Serial myPort) {

  if (myPort == null) {
    return;
  }
  
  if(!deviceReady){
    String input = myPort.readStringUntil('\n');
    input = trim(input);
    println(input);
    deviceReady = "Device is ready".equals(input);
    if(deviceReady){
      setMessage(input, false);
    }
    return;
  }
  
  if(dataToRead <= 0){
    return;
  }
  
  //get string from serial port
  String input = myPort.readStringUntil('\n');
  input = trim(input);
  println(input);  
  dataToRead--;
  
  fullData += "," + input;

  String parts[] = input.split(",");
  float x_acc = 0;
  float y_acc = 0;
  float z_acc = 0;
  float x_gy = 0;
  float y_gy = 0;
  float z_gy = 0;

  try {
    x_acc = Float.parseFloat(parts[0]);
    y_acc = Float.parseFloat(parts[1]);
    z_acc = Float.parseFloat(parts[2]);
    x_gy = Float.parseFloat(parts[3]);
    y_gy = Float.parseFloat(parts[4]);
    z_gy = Float.parseFloat(parts[5]);
  }
  catch(Exception e) {
    setMessage(e.getMessage(), true);
    println(e.getMessage());
  }

  newGesturePlot.setYLim(minY, maxY);

  xaccNew.addPoint(timeStepCounter, x_acc);
  yaccNew.addPoint(timeStepCounter, y_acc);
  zaccNew.addPoint(timeStepCounter, z_acc);
  xgyNew.addPoint(timeStepCounter, x_gy);
  ygyNew.addPoint(timeStepCounter, y_gy);
  zgyNew.addPoint(timeStepCounter, z_gy);

  timeStepCounter++;
  
  
  if(dataToRead == 0){
    setMessage("Data read", false);
  }
  return;
}

void clearGraph() {
  xaccNew.setPoints(new GPointsArray());
  yaccNew.setPoints(new GPointsArray());
  zaccNew.setPoints(new GPointsArray());
  xgyNew.setPoints(new GPointsArray());
  ygyNew.setPoints(new GPointsArray());
  zgyNew.setPoints(new GPointsArray());
  
  timeStepCounter = 0;
}

////////////////////// function for writing to file ////////////////////////////
void writeToFile(String string, FileWriter fw) {
  if (string == null) {
    setMessage("ERROR: No available data", true);
    return;
  }

  try {
    fw.write(string);
    fw.flush();
    setMessage("Data saved to file", false);
  }
  catch(IOException e) {
    setMessage(e.getMessage(), true);
    println("ERROR: Unable to write to file");
  }
}

/////////////////////////////////// functions to print error message ///////////////////////////////////
void setMessage(String message, boolean isError) {
  //messageRectangleHeight = 0;
  messageAvailable = true;
  errorHappened = isError;
  outputString = message;
}

void output_message() {
  if (errorHappened) {
    fill(#F44336);
  } else {
    fill(#8BC34A);
  }
  noStroke();
  if (messageRectangleHeight < 40) {
    messageRectangleHeight+=8;
  }
  rect(0, 0, width, messageRectangleHeight);
  if (messageRectangleHeight == 40) {
    //textSize(18);
    textFont(createFont("Roboto", 16, true));
    textAlign(CENTER);
    fill(255, 255, 255, 255);
    text(outputString, width/2, 25 );
  }
}



////////////////////////////////// mouse events /////////////////////////////////////////////////////////////
// Zoom with mouse wheel
void mouseWheel(MouseEvent event) {
  if (newGesturePlot.isOverBox(mouseX, mouseY)) {
    int delta = (int) event.getAmount();
    float zoomFactor = pow(1.1, -delta);
    float dim[] = newGesturePlot.getDim();
    float plotPos[] = newGesturePlot.getPlotPosAt(mouseX, mouseY);
    float corrX = (plotPos[0] - dim[0] / 2);
    float corrY = (plotPos[1] + dim[1] / 2);
    newGesturePlot.zoom(zoomFactor, mouseX - corrX / zoomFactor, mouseY - corrY / zoomFactor);
  }
}

void mouseDragged() {
  float xMouse = mouseEvent.getX();
  float yMouse = mouseEvent.getY();

  if (panningReferencePoint != null) {
    newGesturePlot.align(panningReferencePoint, xMouse, yMouse);
  } else if (newGesturePlot.isOverBox(xMouse, yMouse)) {
    panningReferencePoint = newGesturePlot.getValueAt(xMouse, yMouse);
  }
}

void mouseReleased() {
  panningReferencePoint = null;
}

////////////////////////////////////// keyboard events ///////////////////////////////////////////////////
void keyPressed() {
  
  if(!deviceReady){
    setMessage("Device is not yet ready", true);
    return;
  }
  if(dataToRead >0){
    setMessage("Data is still reading", true);
    return;
  }
  String gestureName = keyToGestureName.get(key);
  if(gestureName == null){
    if(key == BACKSPACE){
      println("BACKSPACE");
      clearGraph();
      return;
    }
      
    if(key == ENTER){
      println("ENTER");
      clearGraph();
      print(fullData + "\n");
      writeToFile(fullData + "\n", outWriter);
      return;
    }
    
    print(key);
    return;
  }
  clearGraph();
  dataToRead = NUM_OF_TIME_STEPS;
  fullData = gestureName;
  //myPort.write(dataToRead);
  myPort.clear();
  println(gestureName);
  setMessage(gestureName, false);
  return;
}

////////////////////////////////////// function which is called on the end of program ////////////////////////
void stop() {
  try {
    outWriter.close();
  }
  catch(IOException e) {
    println("ERROR: unable to close file");
    e.printStackTrace();
  }
}
