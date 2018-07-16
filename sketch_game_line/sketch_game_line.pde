import controlP5.*;
import oscP5.*;
import netP5.*;

ControlP5 cp5;
OscP5 oscP5;
NetAddress myRemoteLocation;



int x1=50,y1=300,x2=550,y2=300,a1=0,a2=2,t,w=0,rs=0,bs;
void setup(){
  size(600,600);
  frameRate(100);
  background(255);
  textAlign(LEFT,TOP);
  strokeWeight(1.5);
       cp5 = new ControlP5(this);
  
  /* start oscP5, listening for incoming messages at port 12000 */
  oscP5 = new OscP5(this,8000);
}
 
void draw(){
  if(t==0){
    noFill();
    loadPixels();
    stroke(0);
    rect(5,50,width-11,height-56);
    println(pixels[y1*width+(x1+1)]);
    //textSize(20);
    fill(252,110,0);
      //textAlign(LEFT,TOP);
    //text("Orange:"+rs,0,5);
    fill(0,100,255);
      //textAlign(RIGHT,TOP);
      //    text("Blue:"+bs,width,5);
      //    textAlign(CENTER,TOP);
      //    fill(0,255,0);
      //    text("TRON:LIGHT BIKES",300,5);
      //    fill(random(0,255),random(0,255),random(0,255));
      //    text("DIFFICULTY",300,15);
      //    fill(0,random(0,255),0);
      //    text("EASY-press 3",200,25);
      //    fill(0,0,random(0,255));
      //    text("MEDIUM-press 2",290,25);
      //    fill(random(0,255),0,0);
      //    text("HARD-press 1", 380,25);
        
          
          //textAlign(BOTTOM,RIGHT);
          //textAlign(CENTER);
        noFill();
    if(a1==0){
      x1++;
      if(pixels[y1*width+(x1+1)]!=-1){
           bs++;
            t=1;
                    fill(0);
        text("ORANGE HAS BEEN DEFEATED",width/2,height/2);

      }
    }
    else if(a1==1){
      y1--;
      if(pixels[(y1-1)*width+(x1)]!=-1){
        bs++;
           t=1;
                               fill(0);
        text("ORANGE HAS BEEN DEFEATED ",width/2,height/2);
      }
    }
    else if(a1==2){
      x1--;
      if(pixels[y1*width+(x1-1)]!=-1){
        bs++;
            t=1;
           fill(0);
        text("ORANGE HAS BEEN DEFEATED",width/2,height/2);
      }
    }
    else if(a1==3){
      y1++;
      if(pixels[(y1+1)*width+(x1)]!=-1){
        bs++;
             t=1;
                                 fill(0);
        text("ORANGE HAS BEEN DEFEATED",width/2,height/2);
      }
    }
    if(a2==0){
      x2++;
      if(pixels[y2*width+(x2+1)]!=-1){
        rs++;
        fill(0);
        text("BLUE HAS BEEN DEFEATED",width/2,height/2);
             t=1;
      }
    }
    else if(a2==1){
      y2--;
      if(pixels[(y2-1)*width+(x2)]!=-1){
        rs++;
            t=1;
                    fill(0);
        text("BLUE HAS BEEN DEFEATED",width/2,height/2);
      }
    }
    else if(a2==2){
      x2--;
      if(pixels[y2*width+(x2-1)]!=-1){
        rs++;
            t=1;
                    fill(0);
        text("BLUE HAS BEEN DEFEATED",width/2,height/2);
      }
    }
    else if(a2==3){
      y2++;
      if(pixels[(y2+1)*width+(x2)]!=-1){
        rs++;
        t=1;
                fill(0);
        text("BLUE HAS BEEN DEFEATED",width/2,height/2);
      }
    }
    stroke(252,110,0);
    point(x1,y1);
    stroke(0,100,255);
    point(x2,y2);
  }
  else{
   fill(0);
   println(w);
fill(0);
text("Press N for Next Round",width/2,height/2+50);
  t=1;
  x1=50;
  y1=300;
  x2=550;
  y2=300;
  a1=0;
  a2=2;
    if(key== 'n'){
      t=0;
           background(255);
    }
  }
 
 
}
 
void keyPressed() {
  if(keyCode == UP&&a2!=3){
    a2=1;
  }
  else if(keyCode == DOWN&&a2!=1) 
    {a2=3;
  }
  else if(keyCode == LEFT&&a2!=0) {
    a2=2;
  }
  else if (keyCode == RIGHT&&a2!=2) {
    a2=0;
  }
  else if (key == 'w'&&a1!=3) {
    a1=1;
  }
  else if (key == 'a'&&a1!=0) {
    a1=2;
  }
  else if (key == 's'&&a1!=1) {
    a1=3;
  }
  else if (key == 'd'&&a1!=2) {
    a1=0;
  }
  if (key == '1') {frameRate(400);}
  if (key == '2') {frameRate(200);}
  if (key == '3') {frameRate(100);}
  noCursor();
}
void reset(){
 
  
}


   void oscEvent(OscMessage theOscMessage) {  //For communication between Processing and Pure data

  if(theOscMessage.checkAddrPattern("/sinosc")==true) {
  valeur = theOscMessage.get(0).intValue();
  print(valeur);
  }
}
