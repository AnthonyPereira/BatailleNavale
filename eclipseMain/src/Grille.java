
import java.util.Random;
import java.util.Vector;

import javafx.animation.Animation;
import javafx.animation.ParallelTransition;
import javafx.animation.TranslateTransition;
import javafx.scene.Parent;
import javafx.scene.effect.BoxBlur;
import javafx.scene.image.Image;
import javafx.scene.paint.Color;
import javafx.scene.paint.ImagePattern;
import javafx.scene.shape.Rectangle;

public class Grille extends Parent {
	private int taille;
	private double echelle;
	private int x;
	private int y;
	Rectangle fondGrille; // fond noir de la grille
	Tuille[][] listeCase; //creer le tableau avec tout les cases
	Tuille[][] listeCaseFusion;
	Rectangle[][] grilleCaseFond; // petit carr�s pour faire les emplacements de cases
	private static final String FOLDER="SkyPack"; // dossier des images
	private static final Image imageFond =new Image("file:cell/"+FOLDER+"/cellFond.png"); // chemin image de fond
	private static Vector<Animation> fileAnimation= new Vector<Animation>(); // liste des animation en attente
	private static ParallelTransition animationGroupe=new ParallelTransition(); // liste animation globale
	private int score; // score de la grille
	private boolean debug; // affichage des valeurs des cases
	
	public Grille(int x, int y,double echelle,int taille,boolean debug){
		super();
		this.debug=debug;
		this.score=0;
		this.taille=taille;
		this.x=x;
		this.y=y;
		this.echelle=echelle;
		listeCase= new Tuille[taille][taille]; //creer le tableau avec tout les cases
		listeCaseFusion= new Tuille[taille][taille]; // tableau pour gerer les fusion
		fondGrille = new Rectangle();
		fondGrille.setWidth(20*echelle+taille*145*echelle);
		fondGrille.setHeight(20*echelle+taille*145*echelle);
		fondGrille.setX(x);
		fondGrille.setY(y);
		fondGrille.setArcWidth(30*echelle); // coin arrondi sur le haut/bas
		fondGrille.setArcHeight(30*echelle); // coin arrondi sur la gauche/droite
		fondGrille.setFill(Color.BLACK);
		//fondGrille.setEffect(new BoxBlur(30, 20, 3));
		this.getChildren().add(fondGrille);//on ajoute le rectangle au groupe
		grilleCaseFond= new Rectangle[taille][taille];// on creer une table de rectangle pour faire le fond de la table
		for(int i=0;i<taille;i++) {
			for(int j=0;j<taille;j++) {
				grilleCaseFond[i][j]= new Rectangle();
				grilleCaseFond[i][j].setWidth(128*echelle);
				grilleCaseFond[i][j].setHeight(128*echelle);
				grilleCaseFond[i][j].setX(20*echelle+j*145*echelle+x);
				grilleCaseFond[i][j].setY(20*echelle+i*145*echelle+y);
				grilleCaseFond[i][j].setArcWidth(30); // coin arrondi sur le haut/bas
				grilleCaseFond[i][j].setArcHeight(30);
				grilleCaseFond[i][j].setFill(new ImagePattern(imageFond));
				grilleCaseFond[i][j].setEffect(new BoxBlur(10*echelle, 10*echelle, 3));
				this.getChildren().add(grilleCaseFond[i][j]);//on ajoute le rectangle au groupe
			}
		}
	}
	public void reset() throws Exception { // permet de relancer une nouvelle partie
		for(int i=0;i<taille;i++) {
			for(int j=0;j<taille;j++) {
				if(casePlein(i,j)) {
					retirerCase(i,j);
				}
			}
		}
		for(int i=0;i<taille;i++) {
			for(int j=0;j<taille;j++) {
				if(casePlein(i,j)) {
					retirerCaseFusion(i,j);
				}
			}
		}
		fileAnimation.clear(); // on vide la vile d'attente d'animation
		animationGroupe = new ParallelTransition();
		score=0;
		ajouterCase();
		ajouterCase();
	}
	public void actualiserAffichage() { // fonction pour actualiser l'affichage en cas de changement de taille
		fondGrille.setWidth(20*echelle+taille*145*echelle);
		fondGrille.setHeight(20*echelle+taille*145*echelle);
		fondGrille.setArcWidth(30*echelle); // coin arrondi sur le haut/bas
		fondGrille.setArcHeight(30*echelle); // coin arrondi sur la gauche/droite
		//on actualise la grille de fond
		for(int i=0;i<taille;i++) {
			for(int j=0;j<taille;j++) {
				grilleCaseFond[i][j].setWidth(128*echelle);
				grilleCaseFond[i][j].setHeight(128*echelle);
				grilleCaseFond[i][j].setX(20*echelle+j*145*echelle+x);
				grilleCaseFond[i][j].setY(20*echelle+i*145*echelle+y);
				grilleCaseFond[i][j].setArcWidth(30); // coin arrondi sur le haut/bas
				grilleCaseFond[i][j].setArcHeight(30);
				grilleCaseFond[i][j].setFill(new ImagePattern(imageFond));
				grilleCaseFond[i][j].setEffect(new BoxBlur(10*echelle, 10*echelle, 3));
			}
		}
		for(int i=0;i<taille;i++) {
			for(int j=0;j<taille;j++) {
				if(casePlein(i,j)) {
					listeCase[i][j].actualiserAffichage(echelle);
				}
			}
		}
	}
	public void PlacerCase(int i,int j,Tuille tuille) { // remplace le setCase
		listeCase[i][j]=tuille;
	}
	public Rectangle getCase(int i,int j)throws Exception {
		if(listeCase[i][j]!=null) {
			return listeCase[i][j];
		}else {
			throw new Exception("acces a une case inexistante");
		}
	}
	public double getWidth() {
		return fondGrille.getWidth();
	}
	public double getHeight() {
		return fondGrille.getHeight();
	}
	public void setEchelle(double echelle) {
		this.echelle=echelle;
	}
	public int getTaille() {
		return taille;
	}
	public int getCaseValue(int i,int j) throws Exception {
		if(casePlein(i,j)) {
			return (int) listeCase[i][j].getUserData();
		}else {
			throw new Exception("acces données de case inexistantes");
		}
	}
	public  Vector<Animation> getFileAnimation() {
		return fileAnimation;
	}
	public Animation getAnimationGroupe() {
		return animationGroupe;
	}
	public int getScore() {
		return score;
	}
	public void actualiserTableau() throws Exception { //nettois et debug le tableau
		for(int i=0;i<taille;i++) {
			for(int j=0;j<taille;j++) {
				if(casePlein(i,j)) {
					actualiserValeur(i,j,getCaseValue(i,j));
				}
			}
		}
	}
	public void actualiserValeur(int i,int j,int valeur) { // permet de remettre à sa place une case et mettre l'image de sa valeur
		listeCase[i][j].actualiserValeur(valeur);
	}
	public void ajouterCase(int i, int j,int valeur) throws Exception {
		if(listeCase[i][j]==null) {
			listeCase[i][j]=new Tuille(i,j,valeur,x,y,echelle,debug);
			this.getChildren().add(listeCase[i][j]);//on ajoute le rectangle au groupe
			this.getChildren().add(listeCase[i][j].getValeurT());
		}
		else {
			throw new Exception("Case "+i+","+j+" est pleine, impossible ajouter emplacement déjà utilisé");
		}
	}
	public void ajouterCase() throws Exception { //ajouter une case dans le jeu
		if(tablePlein()) {
			throw new Exception("Table Pleine");
		}
		else {
			int i,j;
			Random random= new Random();
			do {
				i=random.nextInt(taille);
				j=random.nextInt(taille);
			}while(casePlein(i,j));
			ajouterCase(i,j,random.nextInt(2)*random.nextInt(2)*random.nextInt(2)*2+2); //petite animation de nouvelle case
			animationZoom(i,j);
		}
	}
	public void ajouterCase(int n) throws Exception { //ajouter une case dans le jeu
		for(int i=0;i<n;i++) {
			if(tablePlein())
				break;
			ajouterCase();
		}
			
	}
	public void animationZoom(int i,int j) {
		listeCase[i][j].animationZoom();
	}
	public boolean tablePlein() {
		for(int i=0;i<taille;i++) {
			for(int j=0;j<taille;j++) {
				if(!casePlein(i,j))
					return false;
			}
		}
		return true;
	}
	//fonction de fin de partie -------------------------------------------
	public boolean perdu() throws Exception {
		return !(testGauche()||testMonter()||testDroite()||testDescendre());
	}
	public boolean gagner() throws Exception{
		for(int i=0;i<taille;i++) {
			for(int j=0;j<taille;j++) {
				if(casePlein(i,j)) {
					if(getCaseValue(i,j)>1024) {
						return true;
					}
				}
			}
		}
		return false;
	}
	//fonction de mouvement de la grille-------------------------------------
	public boolean casePlein(int i, int j) {
		return listeCase[i][j]!=null;
	}
	public boolean casePleinFusion(int i, int j) {
		return listeCase[i][j]!=null;
	}
	public void actualiserPosition(int i,int j) throws InterruptedException { // permet l'animation corrigeant la position de la case
		if(casePlein(i,j)) {
			Animation animation=listeCase[i][j].actualiserPosition();
			if(animation!=null)
				fileAnimation.add(animation);
		}
	}
	public void actualiserPosition() throws InterruptedException {
		for(int i=0;i<taille;i++) {
			for(int j=0;j<taille;j++) {
				actualiserPosition(i,j);
			}
		}
	}
	public void retirerCase(int i, int j) throws Exception { // ne sert plus
		if(casePlein(i,j)) {
			
			this.getChildren().remove(listeCase[i][j]);//on retire le rectangle au groupe
			listeCase[i][j]=null;
		}
		else {
			throw new Exception("Case graphique "+i+","+j+"est null, impossible à retirer, inexistante");
		}
	}
	public void retirerCaseFusion(int i, int j) throws Exception { // ne sert plus
		if(casePleinFusion(i,j)) {
			this.getChildren().remove(listeCaseFusion[i][j]);//on retire le rectangle au groupe
			listeCaseFusion[i][j]=null;
		}
		else {
			throw new Exception("Case graphique "+i+","+j+"est null, impossible à retirer, inexistante");
		}
	}
	public void bougerCase(int posI,int posJ,int cibleI,int cibleJ) throws Exception{ // sert a bouger la position des cases
		if(cibleI==posI && cibleJ==posJ) {
			throw new Exception("Erreur, bouger case au même endroit: "+cibleI+";"+cibleJ);
		}
		else{
			listeCase[posI][posJ].bougerCase(cibleI,cibleJ);
			listeCase[cibleI][cibleJ]=listeCase[posI][posJ];
			listeCase[posI][posJ]=null;
		}
	}
	public void fusionCase(int posI,int posJ,int cibleI,int cibleJ) throws Exception{
		listeCase[posI][posJ].bougerCase(cibleI,cibleJ);
		listeCaseFusion[posI][posJ]=listeCase[posI][posJ]; // on a besoin d'une variable qui existe toujours en dehors de cette fonction pour la supprimer a la fin de l'animation mouvement
		this.getChildren().remove(listeCase[posI][posJ]);
		this.getChildren().add(listeCaseFusion[posI][posJ]);
		listeCase[posI][posJ]=null;
		listeCase[cibleI][cibleJ].setFacteurValeur(2);
		TranslateTransition mouvement=listeCaseFusion[posI][posJ].creerAnimation(cibleI, cibleJ);
		mouvement.setOnFinished(value ->{// se qu'il se passe quand l'animation a fini
			this.getChildren().remove(listeCaseFusion[posI][posJ]); // on oublie la case
			listeCaseFusion[posI][posJ]=null;
		});
		fileAnimation.add(mouvement);
	}
	public void setValeurCase(int i,int j,int valeur) {
		listeCase[i][j].setUserData(valeur);
		actualiserValeur(i,j,valeur);
	}

	// Fonction de test afin de detecter les mouvements mort -----------------------------------
	public boolean testMonterColonne(int j) throws Exception {
		for(int i=0;i<taille-1;i++) {
			if(!casePlein(i,j) && casePlein(i+1,j)) {
				return true;
			}
			else if(casePlein(i+1,j) && casePlein(i,j)){
				if(getCaseValue(i,j)==getCaseValue(i+1,j)) {
					return true;
				}
			}
		}
		return false;
	}
	public boolean testDescendreColonne(int j) throws Exception { //on verifie si on peut bouger
		for(int i=0;i<taille-1;i++) {
			if(!casePlein(i+1,j) && casePlein(i,j)) {
				return true;
			}
			else if(casePlein(i+1,j) && casePlein(i,j)){
				if(getCaseValue(i,j)==getCaseValue(i+1,j)) {
					return true;
				}
			}
		}
		return false;
	}
	public boolean testGaucheLigne(int i) throws Exception {
		for(int j=0;j<taille-1;j++) {
			if(!casePlein(i,j) && casePlein(i,j+1)) {
				return true;
			}
			else if(casePlein(i,j) && casePlein(i,j+1)){
				if(getCaseValue(i,j)==getCaseValue(i,j+1)) {
					return true;
				}
			}
		}
		return false;
	}
	public boolean testDroiteLigne(int i) throws Exception {
		for(int j=0;j<taille-1;j++) {
			if(!casePlein(i,j+1) && casePlein(i,j)) {
				return true;
			}
			else if(casePlein(i,j) && casePlein(i,j+1)){
				if(getCaseValue(i,j)==getCaseValue(i,j+1)) {
					return true;
				}
			}
		}
		return false;
	}
	//test tout les gestes du tableau
	public boolean testMonter() throws Exception {
		for(int i=0;i<taille;i++) {
			if(testMonterColonne(i)) return true;
		}
		return false;
	}
	public boolean testDescendre() throws Exception {
		for(int i=0;i<taille;i++) {
			if(testDescendreColonne(i)) return true;
		}
		return false;
	}
	public boolean testGauche() throws Exception {
		for(int i=0;i<taille;i++) {
			if(testGaucheLigne(i)) return true;
		}
		return false;
	}
	public boolean testDroite() throws Exception {
		for(int i=0;i<taille;i++) {
			if(testDroiteLigne(i)) return true;
		}
		return false;
	}
	public void monterColonne(int j) throws Exception { // bouge la Jeme colonne en haute
		if(testMonterColonne(j)) {
			for(int k=0;k<taille-1;k++) { //pousse les elements
				for(int i=0;i<taille-1;i++) {
					if(!casePlein(i,j) && casePlein(i+1,j)) {
						bougerCase(i+1,j,i,j);
					}
				}
			}
			//for(int k=0;k<taille-1;k++) {//fusionne les elements
			for(int i=0;i<taille-1;i++) {
				if(casePlein(i,j) && casePlein(i+1,j)){
					if(getCaseValue(i,j)==getCaseValue(i+1,j)) {
						score+=getCaseValue(i,j);
						fusionCase(i+1,j,i,j);
					}
				}
			}
			//}
			for(int k=0;k<taille-1;k++) { //repousse les elements SANS LES FUSIONER
				for(int i=0;i<taille-1;i++) {
					if(!casePlein(i,j) && casePlein(i+1,j)) {
						bougerCase(i+1,j,i,j);
					}
				}
			}
		}
	}
	public void descendreColonne(int j) throws Exception { // bouge la Jeme colonne en bas
		if(testDescendreColonne(j)) {
			for(int k=0;k<taille-1;k++) { //pousse les elements
				for(int i=taille-2;i>=0;i--) {
					if(!casePlein(i+1,j) && casePlein(i,j)) {
						bougerCase(i,j,i+1,j);
					}
				}
			}
			//fusionne les elements
			for(int i=taille-2;i>=0;i--) {
				if(casePlein(i,j) && casePlein(i+1,j)){
					if(getCaseValue(i,j)==getCaseValue(i+1,j)) {
						score+=getCaseValue(i,j);
						fusionCase(i,j,i+1,j);
					}
				}
			}
			for(int k=0;k<taille-1;k++) { //repousse les elements SANS LES FUSIONER
				for(int i=taille-2;i>=0;i--) {
					if(!casePlein(i+1,j) && casePlein(i,j)) {
						bougerCase(i,j,i+1,j);
					}
				}
			}
		}
	}
	public void droiteLigne(int i) throws Exception { // bouge la Ieme ligne a droite
		if(testDroiteLigne(i)) {
			for(int k=0;k<taille-1;k++) { //pousse les elements
				for(int j=0;j<taille-1;j++) {
					if(!casePlein(i,j+1) && casePlein(i,j)) {
						bougerCase(i,j,i,j+1);
					}
				}
			}
			//fusionne les elements
			for(int j=taille-2;j>=0;j--) {
				if(casePlein(i,j) && casePlein(i,j+1)){
					if(getCaseValue(i,j)==getCaseValue(i,j+1)) {
						score+=getCaseValue(i,j);
						fusionCase(i,j,i,j+1);
					}
				}
			}
			//}
			for(int k=0;k<taille-1;k++) { //pousse les elements
				for(int j=0;j<taille-1;j++) {
					if(!casePlein(i,j+1) && casePlein(i,j)) {
						bougerCase(i,j,i,j+1);
					}
				}
			}
		}
	}
	public void gaucheLigne(int i) throws Exception { // bouge la Ieme ligne a gauche
		if(testGaucheLigne(i)) {
			for(int k=0;k<taille-1;k++) { //pousse les elements
				for(int j=taille-2;j>=0;j--) {
					if(!casePlein(i,j) && casePlein(i,j+1)) {
						bougerCase(i,j+1,i,j);
					}
				}
			}
			for(int j=0;j<taille-1;j++) {
				if(casePlein(i,j) && casePlein(i,j+1)){
					if(getCaseValue(i,j+1)==getCaseValue(i,j)) {
						score+=getCaseValue(i,j);
						fusionCase(i,j+1,i,j);
					}
				}
			}
			for(int k=0;k<taille-1;k++) { //pousse les elements
				for(int j=taille-2;j>=0;j--) {
					if(!casePlein(i,j) && casePlein(i,j+1)) {
						bougerCase(i,j+1,i,j);
					}
				}
			}
		}
	}
	public void haut() throws Exception { // permet de bouger toutes les cases vers le haut
		for(int i=0;i<taille;i++) {
			monterColonne(i);
		}
	}
	public void bas() throws Exception { // permet de bouger toutes les cases vers le bas
		for(int i=0;i<taille;i++) {
			descendreColonne(i);
		}
	}
	public void gauche() throws Exception { // permet de bouger toutes les cases vers la gauche
		for(int i=0;i<taille;i++) {
			gaucheLigne(i);
		}
	}
	public void droite() throws Exception { // permet de bouger toutes les cases vers la droite
		for(int i=0;i<taille;i++) {
			droiteLigne(i);
		}
	}
	// fonction d�dier aux cartes ---------------------------------------------------------------------
	public boolean testMouvementCarte(int orientation, int sens, int pos) throws Exception {
		if(orientation==0) { // 0 correspond aux colonnes
			if(sens==0) { // 0 correspond vers bas/droite
				return this.testDescendreColonne(pos);
			}else {
				return this.testMonterColonne(pos);
			}
		}else {
			if(sens==0) { // 0 correspond vers bas/droite
				return this.testDroiteLigne(pos);
			}else {
				return this.testGaucheLigne(pos);
			}
		}
	}
	public void mouvementCarte(int orientation, int sens, int pos) throws Exception {
		if(orientation==0) { // 0 correspond aux colonnes
			if(sens==0) { // 0 correspond vers bas/droite
				this.descendreColonne(pos);
			}else {
				this.monterColonne(pos);
			}
		}else {
			if(sens==0) { // 0 correspond vers bas/droite
				this.droiteLigne(pos);
			}else {
				this.gaucheLigne(pos);
			}
		}
	}
	// fonction de r�alisation de chaque tour ----------------------------------------------------
	public void realiserTour(int nbrPop) throws Exception { // fait les op�rations pour actualiser le tableau
		if(!tablePlein())
			ajouterCase(nbrPop);
    	actualiserTableau();
	}
	public void realiserTour() throws Exception {
		realiserTour(1);
	}
	public void jouerAnimationSeq(int nbrPop) throws InterruptedException {
		Animation[] fileAnimationT= new Animation[fileAnimation.size()]; // systeme de conversion Vector<> to tab[]
		for(int i=0;i<fileAnimation.size();i++) {
			fileAnimationT[i]=fileAnimation.get(i);
		}
		fileAnimation.clear(); // on vide la vile d'attente d'animation
		animationGroupe = new ParallelTransition(fileAnimationT);
		animationGroupe.play();
		animationGroupe.setOnFinished(value ->  { // a la fin de l'animation on la vide de tout ses elements
			try {
				animationGroupe.pause();
				animationGroupe = new ParallelTransition();
				this.realiserTour(nbrPop);
			} catch (Exception e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			});
		
	}
}