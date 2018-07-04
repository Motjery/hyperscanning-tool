// WavesOnSphere_1.0
// Instead of click use sound to provoque changes
import controlP5.*;
import oscP5.*;
import netP5.*;

ControlP5 cp5;
OscP5 oscP5;
NetAddress myRemoteLocation;

int Nmax = 1000 ; float M = 50 ; float H = 0.99 ; float HH = 0.01 ;

float X[] = new float[Nmax+1] ; float Y[] = new float[Nmax+1] ; float Z[] = new float[Nmax+1] ;
float V[] = new float[Nmax+1] ; float dV[] = new float[Nmax+1] ; 
float L ; float R = 2*sqrt((4*PI*(200*200)/Nmax)/(2*sqrt(3))) ;
float Lmin ; int N ; int NN ;
float KX ; float KY ; float KZ ;
float KV ; float KdV ; int K ;
int value;
//int filtre = Integer.parseInt(value);

void setup(){
  size(600,600) ;
  background(0,0,0) ;
  noSmooth() ;
  stroke(255,255,255) ;
  fill(50,50,50) ;
  
   cp5 = new ControlP5(this);
  
  
  /* start oscP5, listening for incoming messages at port 12000 */
  oscP5 = new OscP5(this,8000);
  
  for ( N = 0 ; N <= Nmax ; N++ ){
    X[N] = random(-300,+300) ;
    Y[N] = random(-300,+300) ;
    Z[N] = random(-300,+300) ;
  }
  
} // setup()



void draw(){


  background(0,0,0) ;
  
  for ( N = 0 ; N <= Nmax ; N++ ){
     for ( NN = N+1 ; NN <= Nmax ; NN++ ){
        L = sqrt(((X[N]-X[NN])*(X[N]-X[NN]))+((Y[N]-Y[NN])*(Y[N]-Y[NN]))) ;
        L = sqrt(((Z[N]-Z[NN])*(Z[N]-Z[NN]))+(L*L)) ;
        if ( L < R ){
          X[N] = X[N] - ((X[NN]-X[N])*((R-L)/(2*L))) ;
          Y[N] = Y[N] - ((Y[NN]-Y[N])*((R-L)/(2*L))) ;
          Z[N] = Z[N] - ((Z[NN]-Z[N])*((R-L)/(2*L))) ;
          X[NN] = X[NN] + ((X[NN]-X[N])*((R-L)/(2*L))) ;
          Y[NN] = Y[NN] + ((Y[NN]-Y[N])*((R-L)/(2*L))) ;
          Z[NN] = Z[NN] + ((Z[NN]-Z[N])*((R-L)/(2*L))) ;
          dV[N] = dV[N] + ((V[NN]-V[N])/M) ;
          dV[NN] = dV[NN] - ((V[NN]-V[N])/M) ;
          stroke(100+(Z[N]/2),160+(Z[N]/2),150+(Z[N]/2)) ; 
          line(X[N]*1.2*(100+V[N])/200+300,Y[N]*1.2*(100+V[N])/200+300,X[NN]*1.2*(100+V[NN])/200+300,Y[NN]*1.2*(100+V[NN])/200+300) ; 
        }
        if ( Z[N] > Z[NN] ){
          KX = X[N] ; KY = Y[N] ; KZ = Z[N] ; KV = V[N] ; KdV = dV[N] ; 
          X[N] = X[NN] ; Y[N] = Y[NN] ; Z[N] = Z[NN] ; V[N] = V[NN] ; dV[N] = dV[NN] ;  
          X[NN] = KX ; Y[NN] = KY ; Z[NN] = KZ ; V[NN] = KV ; dV[NN] = KdV ; 
        }
     }
     L = sqrt((X[N]*X[N])+(Y[N]*Y[N])) ;
     L = sqrt((Z[N]*Z[N])+(L*L)) ;
     X[N] = X[N] + (X[N]*(200-L)/(2*L)) ;
     Y[N] = Y[N] + (Y[N]*(200-L)/(2*L)) ;
     Z[N] = Z[N] + (Z[N]*(200-L)/(2*L)) ;
     KZ = Z[N] ; KX = X[N] ;
     Z[N] = (KZ*cos(float(300-150)/10000))-(KX*sin(float(300-150)/10000)) ;
     X[N] = (KZ*sin(float(300-150)/10000))+(KX*cos(float(300-150)/10000)) ;
     KZ = Z[N] ; KY = Y[N] ;
     Z[N] = (KZ*cos(float(300-0)/10000))-(KY*sin(float(300-0)/10000)) ;
     Y[N] = (KZ*sin(float(300-0)/10000))+(KY*cos(float(300-0)/10000)) ;
     dV[N] = dV[N] - (V[N]*HH) ; 
     V[N] = V[N] + dV[N] ; dV[N] = dV[N] * H ;
  }



  Lmin = 600 ; NN = 0 ;
  for ( N = 0 ; N <= Nmax ; N++ ){
     L = sqrt(((100-(300+X[N]))*(150-(300+X[N])))+((0-(300+Y[N]))*(0-(300+Y[N])))) ;
     if ( Z[N] > 0 && L < Lmin ){ NN = N ; Lmin = L ; }
  }
  
  //if(value == 130){
  //    if ( K == 0){ dV[NN] = -0 ; K = 1 ; }
  //         else{ dV[NN] = +0 ; K = 0 ; }
  //}
  if(value == 120){
      if ( K == 0 ){ dV[NN] = -0 ; K = 1 ; }
           else{ dV[NN] = +0 ; K = 0 ; }
  }
  if(value == 110){
      if ( K == 0 ){ dV[NN] = -0 ; K = 1 ; }
           else{ dV[NN] = +0 ; K = 0 ; }
  }
  if(value == 100){
      if ( K == 0 ){ dV[NN] = -4 ; K = 1 ; }
           else{ dV[NN] = +4 ; K = 0 ; }
  }
  if(value == 90){
      if ( K == 0 ){ dV[NN] = -8 ; K = 1 ; }
           else{ dV[NN] = +8 ; K = 0 ; }
  }
  if(value == 80){
      if ( K == 0 ){ dV[NN] = -15 ; K = 1 ; }
           else{ dV[NN] = +15 ; K = 0 ; }
  }
  if(value == 70){
      if ( K == 0 ){ dV[NN] = -30 ; K = 1 ; }
           else{ dV[NN] = +30 ; K = 0 ; }
  }
  if(value == 60){
      if ( K == 0 ){ dV[NN] = -40 ; K = 1 ; }
           else{ dV[NN] = +40 ; K = 0 ; }
  }
  if(value == 50){
      if ( K == 0 ){ dV[NN] = -80 ; K = 1 ; }
           else{ dV[NN] = +80 ; K = 0 ; }
  }
  //if(value == 40){è
  //    if ( K == 0 ){ dV[NN] = -40 ; K = 1 ; }
  //         else{ dV[NN] = +40 ; K = 0 ; }
  //}
  //if(value == 30){
  //    if ( K == 0 ){ dV[NN] = -45 ; K = 1 ; }
  //         else{ dV[NN] = +45 ; K = 0 ; }
  //}
  //if(value == 20){
  //    if ( K == 0 ){ dV[NN] = -50 ; K = 1 ; }
  //         else{ dV[NN] = +50 ; K = 0 ; }
  //}
 /* if(value == 12){
      if ( K == 0 ){ dV[NN] = -55 ; K = 1 ; }
           else{ dV[NN] = +55 ; K = 0 ; }
  }
  if(value == 13){
      if ( K == 0 ){ dV[NN] = -60 ; K = 1 ; }
           else{ dV[NN] = +60 ; K = 0 ; }
  }*/
}


      void oscEvent(OscMessage theOscMessage) {  //For communication between Processing and Pure data

  if(theOscMessage.checkAddrPattern("/sinosc")==true) {
  value = theOscMessage.get(0).intValue();
  print(value);
  }
  }
