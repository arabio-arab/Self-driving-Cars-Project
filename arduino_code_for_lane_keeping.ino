#include <HCSR04.h>
UltraSonicDistanceSensor distanceSensor(13,12);  // Initialize sensor that uses digital pins 13 and 12.
// Définition des broches pour le contrôle des moteurs
const int ENA = 6; // Broche de contrôle de la vitesse du moteur A
const int IN1 = 2;
const int IN2 = 7;
const int IN3 = 4;
const int IN4 = 5;
const int ENB = 9; // Broche de contrôle de la vitesse du moteur B
const int capteurIR1 = A0;   /// trajet
const int capteurIR2 = A3; //trajet 

const int capteurIR3 = A1;  // suiveur de ligne
const int capteurIR4 = A2; //suiveur de ligne a droit

int data;

int nombre_detection_1ere = 0; // Variable pour stocker le nombre de détections de la première condition
int nombre_detection_2eme = 0; // Variable pour stocker le nombre de détections de la deuxième condition
bool premiere_condition = false; // Variable pour indiquer si la première condition est satisfaite

void setup() {
  // Définition des broches en sortie
  Serial.begin(38400);
  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(ENB, OUTPUT);
}

void loop() {
  // Déclaration des variables
  delay(100);
  float distance = distanceSensor.measureDistanceCm();
  int valeurIR1, valeurIR2;
  int valeurIR3,valeurIR4;
  
  // Vérification de la réception de données série
  while(Serial.available() > 0) {
    data = Serial.read();
  // Boucle principale
   
   if (data == 'D') {
  Serial.print(data);
   
   while (true) {
    // Faire une mesure à l'aide du capteur toutes les 500 millisecondes et afficher la distance en centimètre

    // Lecture de la valeur du capteur infrarouge
    valeurIR1 = analogRead(capteurIR1);
    valeurIR2 = analogRead(capteurIR2);
    valeurIR3 = analogRead(capteurIR3);
    valeurIR4 = analogRead(capteurIR4);


    // Affichage de la valeur lue dans le moniteur série
    Serial.print("R1: ");
    Serial.print(valeurIR1);
    Serial.print(" R2: ");
    Serial.print(valeurIR2);
    
     Serial.print(" R3: ");
     Serial.print(valeurIR3);
     Serial.print(" R4: ");
     Serial.println(valeurIR4);

    // Vérifier si la première condition est remplie
    if (valeurIR3 >250 && valeurIR4 >250) {
      if (!premiere_condition) {
        nombre_detection_1ere++; // Incrémenter le compteur de la première condition
        premiere_condition = true; // Marquer que la première condition est remplie
      }
    } else {
      premiere_condition = false; // Réinitialiser la première condition si elle n'est plus satisfaite
    }

    // Afficher le nombre de détections pour chaque condition
  //  Serial.print("1ere nombre de detection: ");
  //  Serial.println(nombre_detection_1ere);
  //  Serial.print("2eme nombre de detection: ");
   // Serial.println(nombre_detection_2eme);

    // Sortir de la boucle après un certain nombre de détections de la deuxième condition
    if (nombre_detection_1ere >= 2) {
      break;
    }

    // Contrôle des moteurs en fonction des valeurs des capteurs infrarouges
    if (valeurIR3  <300 && valeurIR4 <300) {
      
      // Avancer
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, HIGH);
      digitalWrite(IN3, HIGH);
      digitalWrite(IN4, LOW);
      // Vitesse constante pour les moteurs A et B
      analogWrite(ENA, 50); // Exemple de PWM pour la vitesse du moteur A
      analogWrite(ENB, 45); // Exemple de PWM pour la vitesse du moteur B

    } else if (valeurIR3 >300 && valeurIR4 <300) {
      // Tourner à gauche
      digitalWrite(IN1, HIGH);
      digitalWrite(IN2, LOW);
      digitalWrite(IN3, HIGH);
      digitalWrite(IN4, LOW);
       
      // Vitesse constante pour les moteurs A et B
      analogWrite(ENA, 85); // Exemple de PWM pour la vitesse du moteur A
      analogWrite(ENB, 80); // Exemple de PWM pour la vitesse du moteur B

    } else if (valeurIR3 <300 && valeurIR4 >300) {

       digitalWrite(IN1, LOW);
      digitalWrite(IN2, HIGH);
      digitalWrite(IN3, LOW);
      digitalWrite(IN4, HIGH);

      // Vitesse constante pour les moteurs A et B
      analogWrite(ENA, 85); // Exemple de PWM pour la vitesse du moteur A
      analogWrite(ENB, 80); // Exemple de PWM pour la vitesse du moteur B

    } else if (valeurIR3 >300 && valeurIR4 >300) {
      //      Reculer
     digitalWrite(IN1, LOW);
     digitalWrite(IN2, HIGH);
     digitalWrite(IN3, LOW);
     digitalWrite(IN4, HIGH);
      
      // Vitesse constante pour les moteurs A et B
      analogWrite(ENA, 180); // Exemple de PWM pour la vitesse du moteur A
      analogWrite(ENB, 175); // Exemple de PWM pour la vitesse du moteur B
 
    }
 }
 // le debuit de la deuxieme trajet les condition ici changer par ce que le  premiere trajet est deferent par rapport a la 2eme



 
    Serial.println(distance);
 
      if (valeurIR1 >300 && valeurIR2<300 ){
      digitalWrite(IN1, HIGH);
      digitalWrite(IN2, LOW);
      digitalWrite(IN3, HIGH);
      digitalWrite(IN4, LOW);
      // Vitesse variable pour les moteurs A et B
      analogWrite(ENA, 70); // Exemple de PWM pour la vitesse du moteur A
      analogWrite(ENB, 65); // Exemple de PWM pour la vitesse du moteur B
      }
      else if (valeurIR1 >300 && valeurIR2 >300 ){
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, HIGH);
      digitalWrite(IN3, HIGH);
      digitalWrite(IN4, LOW);
      // Vitesse variable pour les moteurs A et B
      analogWrite(ENA, 65); // Exemple de PWM pour la vitesse du moteur A
      analogWrite(ENB, 60); // Exemple de PWM pour la vitesse du moteur B

      }
      else if (valeurIR1 <300 && valeurIR2 <300 ){
      digitalWrite(IN1, HIGH);
      digitalWrite(IN2, LOW);
      digitalWrite(IN3, LOW);
      digitalWrite(IN4, HIGH);
      // Vitesse variable pour les moteurs A et B
      analogWrite(ENA, 65); // Exemple de PWM pour la vitesse du moteur A
      analogWrite(ENB, 60); // Exemple de PWM pour la vitesse du moteur B

      }
      else if (valeurIR1 <300 && valeurIR2 >300){
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, HIGH);
      digitalWrite(IN3, LOW);
      digitalWrite(IN4, HIGH);
      // Vitesse variable pour les moteurs A et B
      analogWrite(ENA, 70); // Exemple de PWM pour la vitesse du moteur A
      analogWrite(ENB, 65); // Exemple de PWM pour la vitesse du moteur B
      }
       if(distance>20 || distance>-1){
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, LOW);
      digitalWrite(IN3, LOW);
      digitalWrite(IN4, LOW);
      analogWrite(ENA, 0); // Exemple de PWM pour la vitesse du moteur A
      analogWrite(ENB, 0);
   }
  }
  if(data=='p'){//Passage pieton
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, 55); // Exemple de PWM pour la vitesse du moteur A
  analogWrite(ENB, 50); // Exemple de PWM pour la vitesse du moteur B  
   }
      
  if (data=='g'){//  Light is green
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, HIGH);
    digitalWrite(IN3, HIGH);
    digitalWrite(IN4, LOW);
    analogWrite(ENA, 65); // Exemple de PWM pour la vitesse du moteur A
    analogWrite(ENB, 60); // Exemple de PWM pour la vitesse du moteur B
  }
  if(data=='y'){ //  Light is Yellow
   digitalWrite(IN1, HIGH);
   digitalWrite(IN2, LOW);
   digitalWrite(IN3, HIGH);
   digitalWrite(IN4, LOW);
   analogWrite(ENA, 55); // Exemple de PWM pour la vitesse du moteur A
   analogWrite(ENB, 50); // Exemple de PWM pour la vitesse du moteur B
  }
   if(data=='r'){ //  Light is Read
   digitalWrite(IN1, LOW);
   digitalWrite(IN2, LOW);
   digitalWrite(IN3, LOW);
   digitalWrite(IN4, LOW);
   analogWrite(ENA, 0); // Exemple de PWM pour la vitesse du moteur A
   analogWrite(ENB, 0); // Exemple de PWM pour la vitesse du moteur B
  }
   if(data=='i'){ //  interdit on peut modifier le range de cette operation
   digitalWrite(IN1, LOW);
   digitalWrite(IN2, HIGH);
   digitalWrite(IN3, LOW);
   digitalWrite(IN4, HIGH);
   analogWrite(ENA, 70); // Exemple de PWM pour la vitesse du moteur A
   analogWrite(ENB, 75); // Exemple de PWM pour la vitesse du moteur B
  }
  if(data=='s'){//Stop
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, 55); // Exemple de PWM pour la vitesse du moteur A
  analogWrite(ENB, 50); // Exemple de PWM pour la vitesse du moteur B  
  delay(5000);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, 65); // Exemple de PWM pour la vitesse du moteur A
  analogWrite(ENB, 60); // Exemple de PWM pour la vitesse du moteur B
  }
  if(data=='n'){//turn right
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  analogWrite(ENA, 70); // Exemple de PWM pour la vitesse du moteur A
  analogWrite(ENB, 75); // Exemple de PWM pour la vitesse du moteur B
 }
}
}