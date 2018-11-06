//This sketch is available in open source on openprocessing.org
import controlP5.*;
import oscP5.*;
import netP5.*;

//ControlP5 to connect Pure data to Processing
ControlP5 cp5;
OscP5 oscP5;
NetAddress myRemoteLocation;

//Sphere parametre
int Nmax = 500 ; float M = 50 ; float H = 0.99 ; float HH = 0.01 ;
float X[] = new float[Nmax+1] ; float Y[] = new float[Nmax+1] ; float Z[] = new float[Nmax+1] ;
float V[] = new float[Nmax+1] ; float dV[] = new float[Nmax+1] ; 
float L ; float R = 2*sqrt((4*PI*(200*200)/Nmax)/(2*sqrt(3))) ;
float Lmin ; int N ; int NN ;
float KX ; float KY ; float KZ ;
float KV ; float KdV ; int K ;

//Value is send by pure data to create the sphere distorsion
int value;

void setup(){
  size(600,600) ;
  background(0,0,0) ;
  noSmooth() ;
  stroke(255,255,255) ;
  fill(50,50,50) ;
  
  for ( N = 0 ; N <= Nmax ; N++ ){
    X[N] = random(-300,+300) ;
    Y[N] = random(-300,+300) ;
    Z[N] = random(-300,+300) ;
  }
  
    // start oscP5, listening for incoming messages at port 8000
  cp5 = new ControlP5(this);
  oscP5 = new OscP5(this,8000);
  
} //end of setup()



void draw(){
  background(0,0,0) ;
  //Create the sphere
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
  
  //Distorsion is more or less important in function of value
  //No distorsion with 17, 18 and 19
  if(value == 17 || value == 18 || value == 19){
      if ( K == 0 ){ dV[NN] = -0 ; K = 1 ; }
           else{ dV[NN] = +0 ; K = 0 ; }
    }
    //dv[NN] allows to modify the distorsion
  if(value == 16){
      if ( K == 0 ){ dV[NN] = -2 ; K = 1 ; }
           else{ dV[NN] = +2 ; K = 0 ; }
    }
  if(value == 15){
      if ( K == 0 ){ dV[NN] = -4 ; K = 1 ; }
           else{ dV[NN] = +4 ; K = 0 ; }
    }
  if(value == 14){
      if ( K == 0 ){ dV[NN] = -8 ; K = 1 ; }
           else{ dV[NN] = +8 ; K = 0 ; }
    }
  if(value == 13){
      if ( K == 0 ){ dV[NN] = -12 ; K = 1 ; }
           else{ dV[NN] = +12 ; K = 0 ; }
    }
  if(value == 12){
      if ( K == 0 ){ dV[NN] = -15 ; K = 1 ; }
           else{ dV[NN] = +15 ; K = 0 ; }
    }
  if(value == 11){
      if ( K == 0 ){ dV[NN] = -20 ; K = 1 ; }
           else{ dV[NN] = +20 ; K = 0 ; }
    }
  if(value == 10){
      if ( K == 0 ){ dV[NN] = -25 ; K = 1 ; }
           else{ dV[NN] = +25 ; K = 0 ; }
    }  
}//end of draw


//Reception of int value
      void oscEvent(OscMessage theOscMessage) {  //For communication between Processing and Pure data

  if(theOscMessage.checkAddrPattern("/sinosc")==true) {
  value = theOscMessage.get(0).intValue();
  print(value);
  }
  }