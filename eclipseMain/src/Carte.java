import java.util.Random;

import javafx.animation.Animation.Status;
import javafx.scene.Parent;
import javafx.scene.control.Button;
import javafx.scene.paint.Color;
import javafx.scene.shape.Rectangle;

public class Carte extends Parent {
	private int nbrMove; // nombre d'action disponible pour le bonus
	private int hauteur; // la hauteur du bouton bonus
	private static final int LARGEUR=200; // largeur fixe du bouton
	private int[][] listeMove; // lsite des actions que donne le bonus
	private int x;
	private int y;
	private Button bouton;
	private Rectangle fond;
	public Carte(int x, int y,Grille grille) {
		super();
		nbrMove=(int) grille.getTaille()/2;
		hauteur=nbrMove*21;
		fond = new Rectangle();
		bouton = new Button("Utiliser Carte");
		this.x=x; // pos en X de la carte
		this.y=y; // pos en Y de la carte
		 // nombre d'action proposé par la carte
		this.listeMove = new int[nbrMove][3]; // liste des actions proposé par la carte
		fond.setWidth(LARGEUR);
		fond.setHeight(hauteur);
		fond.setX(x);
		fond.setY(y);
		bouton.setLayoutX(x);
		bouton.setLayoutY(y);
		bouton.setPrefSize(LARGEUR, hauteur);
		bouton.setOnAction(value ->  { // action du bouton reset
			try {
				utiliserCarte(grille);
			} catch (Exception e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
         });
		fond.setArcWidth(5); // coin arrondi sur le haut/bas
		fond.setArcHeight(5); // coin arrondi sur la gauche/droite
		fond.setFill(Color.GREY);
		this.getChildren().add(fond);
		this.getChildren().add(bouton);
	}
	// tout les get
	public int getHauteur() {
		return hauteur;
	}
	public static int getLargeur() {
		return LARGEUR;
	}
	public int getNbrMove() {
		return nbrMove;
	}
	public int[][] getListeMove() {
		return listeMove;
	}
	public int getX() {
		return x;
	}
	public int getY() {
		return y;
	}
	public void actualiserAffichage(int x, int y) {
		this.x=x; // pos en X de la carte
		this.y=y; // pos en Y de la carte
		 // nombre d'action proposé par la carte
		fond.setWidth(LARGEUR); // taille en largeur
		fond.setHeight(hauteur); // taille en hauteur
		fond.setX(x);
		fond.setY(y);
		bouton.setLayoutX(x);
		bouton.setLayoutY(y);
		bouton.setPrefSize(LARGEUR, hauteur);
	}
	public void actualiserListeMove(Grille grille) throws Exception { // permet de changer les ordres d'une case
		int orientation;
		int sens;
		int pos;
		Random random=new Random();
		//Grille grilleClone= grille;
		bouton.setText("");
		String tmp="";
		orientation=random.nextInt(2); // permet d'avoir tout les mouvements d'une carte en colonnes ou lignes
		for(int i=0;i<nbrMove;i++) {
			//do {
			sens=random.nextInt(2); // dis dans quel orientation part le mouvement
			pos=random.nextInt(grille.getTaille()); // on donne la colonne ou ligne affecté par le mouvement
			//}while(!grille.testMouvementCarte(orientation,sens,pos)); //!grilleClone.testMouvementCarte(orientation,sens,pos)
			//listeMove[i]= {orientation,sens,pos};
			listeMove[i][0]=orientation;
			listeMove[i][1]=sens;
			listeMove[i][2]=pos;
			
			if(orientation==0) { // 0 correspond aux colonnes
				if(sens==0) { // 0 correspond vers bas/droite
					if(pos==0)
						tmp+="1ère colonne vers le bas\n";
					else
						tmp+=(pos+1)+"ème colonne vers le bas\n";
				}else {
					if(pos==0)
						tmp+="1ère colonne vers le haut\n";
					else
						tmp+=(pos+1)+"ème colonne vers le haut\n";
				}
			}else {
				if(sens==0) { // 0 correspond vers bas/droite
					if(pos==0)
						tmp+="1ère ligne vers la droite\n";
					else
						tmp+=(pos+1)+"ème ligne vers la droite\n";
				}else {
					if(pos==0)
						tmp+="1ère ligne vers la gauche\n";
					else
						tmp+=(pos+1)+"ème ligne vers la gauche\n";
				}
			}
			//grilleClone.mouvementCarte(orientation,sens,pos);
		}
		bouton.setText(tmp);
	}
	public void utiliserCarte(Grille grille) throws Exception { // permet d'appliquer les changements spécifié par la carte
		if(grille.getAnimationGroupe().getStatus()!= Status.RUNNING && !grille.gagner() && !grille.perdu()) {
			for(int i=0;i<nbrMove;i++) {
					grille.mouvementCarte(listeMove[i][0],listeMove[i][1],listeMove[i][2]);
			}
			actualiserListeMove(grille);
		}
	}
}
