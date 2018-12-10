import javafx.animation.ScaleTransition;
import javafx.animation.TranslateTransition;
import javafx.scene.image.Image;
import javafx.scene.paint.Color;
import javafx.scene.paint.ImagePattern;
import javafx.scene.shape.Rectangle;
import javafx.scene.text.Font;
import javafx.scene.text.Text;
import javafx.util.Duration;

public class Tuille extends Rectangle {
	private static final String FOLDER="SkyPack";
	private static final String FORMAT="gif";
	private static final Image[] LISTEIMAGE={
		new Image("file:cell/"+FOLDER+"/cell2."+FORMAT),
		new Image("file:cell/"+FOLDER+"/cell4."+FORMAT),
		new Image("file:cell/"+FOLDER+"/cell8."+FORMAT),
		new Image("file:cell/"+FOLDER+"/cell16."+FORMAT),
		new Image("file:cell/"+FOLDER+"/cell32."+FORMAT),
		new Image("file:cell/"+FOLDER+"/cell64."+FORMAT),
		new Image("file:cell/"+FOLDER+"/cell128."+FORMAT),
		new Image("file:cell/"+FOLDER+"/cell256."+FORMAT),
		new Image("file:cell/"+FOLDER+"/cell512."+FORMAT),
		new Image("file:cell/"+FOLDER+"/cell1024."+FORMAT),
		new Image("file:cell/"+FOLDER+"/cell2048."+FORMAT),
		new Image("file:cell/"+FOLDER+"/cell4096."+FORMAT)};
	private Text valeurT; // texte d'affichage de la case
	private double echelle; // echelle du tableau
	private int i;// position dans le tableau
	private int j;// position dans le tableau
	private int margeX;// marge du tableau ou on va mettre les valeurs
	private int margeY;// marge du tableau ou on va mettre les valeurs
	private int facteurValeur; // permet d'augmenter la valeur de la case en cas de fusion
	private boolean debug;// permet afficher valeur des cases
	public Tuille(int i,int j,int valeur, int margeX, int margeY, double echelle,boolean debug) {
		super();
		this.debug=debug;
		this.echelle=echelle;
		this.i=i;
		this.j=j;
		this.margeX=margeX;
		this.margeY=margeY;
		valeurT=new Text(valeur+"");
		valeurT.setFont(new Font(20));
		valeurT.setFill(Color.TRANSPARENT);
		if(debug)
			valeurT.setFill(Color.WHEAT);
		this.setWidth(128*echelle);
		this.setHeight(128*echelle);
		this.setArcWidth(30/4); // coin arrondi sur le haut/bas
		this.setArcHeight(30/4);
		this.actualiserValeur( i, j,valeur);
		this.setUserData(valeur);
		facteurValeur=1;
	}
	public Text getValeurT() {
		return valeurT;
	}
	public int racineBinaire(int valeur) {
		int racine=valeur;
		int tour=0;
		while(racine>1) {
			racine/=2;
			tour++;
		}
		return tour;
	}
	public void setFacteurValeur(int facteur) { // change la valeur quand il y a une fusion
		facteurValeur=facteur;
	}
	public void actualiserValeur(int i,int j,int valeur) { // permet de remettre à sa place une case et mettre l'image de sa valeur
		this.setX(20*echelle+j*145*echelle+margeX);
		this.setY(20*echelle+i*145*echelle+margeY);
		valeurT.setLayoutX(this.getX()+4);
		valeurT.setLayoutY(this.getY()+20);
		if(facteurValeur>1){
			this.setUserData(valeur*facteurValeur);
			valeurT.setText(""+this.getUserData());
			facteurValeur=1;
		}
		this.setFill(new ImagePattern(LISTEIMAGE[racineBinaire(valeur)-1]));
	}
	public void repositionnerTuille() { // retire la transition en cours
		this.setTranslateX(0);
		this.setTranslateY(0);
	}
	public void actualiserValeur(int valeur) { // actualise X et Y
		actualiserValeur(i,j,valeur);
		repositionnerTuille();
	}
	public void actualiserValeur() {
		actualiserValeur(i,j,(int)this.getUserData());
	}
	public void bougerCase(int i,int j) {
		this.i=i;
		this.j=j;
	}
	public TranslateTransition actualiserPosition() { // creer le mouvement pour faire les animations a l'écran
		double posX=this.getX();
		double posY=this.getY();
		double cibleX=20*echelle+j*145*echelle+margeX;
		double cibleY=20*echelle+i*145*echelle+margeY;
		if(cibleX!=posX || cibleY!=posY) {
			TranslateTransition translateTransition = new TranslateTransition(Duration.millis(250),this);
			translateTransition.setByX(cibleX-posX);
			translateTransition.setByY(cibleY-posY);
			valeurT.setFill(Color.TRANSPARENT);
			translateTransition.setOnFinished(value ->  {
				if(debug)
					valeurT.setFill(Color.WHEAT);
			});
			return translateTransition;
		}
		actualiserValeur();
		return null;
	}
	public TranslateTransition creerAnimation(int cibleI,int cibleJ) { // animation pour la fusion
		double posX=this.getX();
		double posY=this.getY();
		double cibleX=20*echelle+cibleJ*145*echelle+margeX;
		double cibleY=20*echelle+cibleI*145*echelle+margeY;
		if(cibleX!=posX || cibleY!=posY) {
			TranslateTransition translateTransition = new TranslateTransition(Duration.millis(250),this);
			translateTransition.setByX(cibleX-posX);
			translateTransition.setByY(cibleY-posY);
			valeurT.setFill(Color.TRANSPARENT);
			translateTransition.setOnFinished(value ->  {
				this.animationZoom();
				if(debug)
					valeurT.setFill(Color.WHEAT);
			});
			this.animationZoom();
			return translateTransition;
		}
		
		//repositionnerTuille();
		return null;
	}
	public void animationZoom() { // permet de lancer l'animation de zoom lors de la fusion et le pop dune nouvelle
		ScaleTransition st = new ScaleTransition(Duration.millis(100), this);
		st.setFromX(1);
		st.setFromY(1);
		st.setToX(1.5);
	    st.setToY(1.5);
	    st.setCycleCount(2);
	    st.setAutoReverse(true);
	    st.play();
	}
	public void actualiserAffichage(double echelle) { // remet a l'echelle la fenetre si elle change de taille
		this.echelle=echelle;
		this.setWidth(128*echelle);
		this.setHeight(128*echelle);
		this.actualiserValeur(i,j,(int)getUserData());
		valeurT.setX(this.getX()+this.getWidth()-15);
		valeurT.setY(this.getY()+20);
	}
}
