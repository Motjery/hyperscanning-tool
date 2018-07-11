import controlP5.*;
import oscP5.*;
import netP5.*;

ControlP5 cp5;
OscP5 oscP5;
NetAddress myRemoteLocation;

int valeur;


Snake s;
int scl = 20;

PVector food;

void setup() {
  size(600, 600);
  s = new Snake();
  frameRate(4);
  pickLocation();
     cp5 = new ControlP5(this);
  
  
  /* start oscP5, listening for incoming messages at port 12000 */
  oscP5 = new OscP5(this,8000);
}

void pickLocation() {
  int cols = width/scl;
  int rows = height/scl;
  food = new PVector(floor(random(cols)), floor(random(rows)));
  food.mult(scl);
}

void mousePressed() {
  s.total++;
}

void draw() {
  background(51);

  if (s.eat(food)) {
    pickLocation();
  }
  s.death();
  s.update();
  s.show();


  fill(255, 0, 100);
  rect(food.x, food.y, scl, scl);



  if (valeur == 2) {//haut
    s.dir(0, -1);
  } else if (valeur == 4) {//bas
    s.dir(0, 1);
  } else if (valeur == 1) {//droite
    s.dir(1, 0);
  } else if (valeur == 3) {//gauche
    s.dir(-1, 0);
  }
}
   void oscEvent(OscMessage theOscMessage) {  //For communication between Processing and Pure data

  if(theOscMessage.checkAddrPattern("/sinosc")==true) {
  valeur = theOscMessage.get(0).intValue();
  print(valeur);
  }
}
