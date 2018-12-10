
import javafx.application.Application;
import javafx.event.EventHandler;
import javafx.scene.Group;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.CheckBox;
import javafx.scene.control.Separator;
import javafx.scene.control.Slider;
import javafx.scene.control.ToolBar;
import javafx.scene.image.ImageView;
import javafx.scene.paint.Color;
import javafx.scene.text.Font;
import javafx.scene.text.Text;
import javafx.stage.Stage;

import javafx.animation.Animation.Status;
import javafx.animation.AnimationTimer;
import javafx.scene.input.KeyEvent;

public class Fenetre extends Application{
	private Text zoneScore; // zone d'affichage de score dans la barre d'outils
	private Grille grilleJeu; // zone de jeu
	final String imageURL ="file:cell/DestroyerXpl.png"; // fond de fenetre
	final String bonusURL ="file:cell/bonus.png"; // fond de fenetre
	private final ImageView imageBonus = new ImageView(bonusURL); // zone de fond de fenetre pour scene principale
	private final ImageView imageView = new ImageView(imageURL); // zone de fond de fenetre pour scene principale
    private  final ImageView fondOption = new ImageView(imageURL); // zone de fond de fenetre pour les options
	private int nbrCarte=4; // nombres de carte bonus
	private Carte[] listeCarte; // liste des cartes bonus
	private Group root; // racine principale
	private Scene scene; // scene principale
	private boolean haut,bas,gauche,droite,move; // keylistener pour hautbasGaucheDroite + si on a boug�
	private int tailleTableau=4; // taille du tableau initial
	private ToolBar toolBar; // la barre d'outil de la fenetre initial
	private Text gameOver; // affichage de fin de partie
	private int nbrPop=1; // nombre de nouvelle case � chaque tour
	private boolean debug=false; // permet d'afficher la valeur des cases
	private static final int MAXGRILLE=10;
	
    @Override
    public void start(Stage primaryStage) throws Exception { // initialisation de l'interface et fonction liées au boutons et autre
    	root = new Group();
        scene = new Scene(root, 800, 600, Color.DARKSLATEBLUE); // la fenetre window
        root.getChildren().add(imageView); 
        grilleJeu = new Grille(50, 50, 0.8*(double)(4.0/tailleTableau),tailleTableau,debug); // position de la grille
        grilleJeu.reset();
        scene.widthProperty().addListener((obs, oldVal, newVal) -> {
            actualiserAffichage(grilleJeu);
        });
        scene.heightProperty().addListener((obs, oldVal, newVal) -> {
        	actualiserAffichage(grilleJeu);
        });
        root.minHeight(600);
        root.minWidth(400);
        imageView.setFitWidth(scene.getWidth()); // on met en pleine fenetre l'image de fond
        imageView.setFitHeight(scene.getHeight()); 
        zoneScore = new Text(actualiserScore()); // zone d'affichage du score
        Font fontScore=new Font(15); //les fonts
    	Font font=new Font(50);
        primaryStage.setTitle("2048 - PlayerCard edition");
        listeCarte= new Carte[nbrCarte];
        imageBonus.setX((int) scene.getWidth()-250);
        imageBonus.setY(50);
        imageBonus.setFitWidth(200);
        for(int i=0;i<nbrCarte;i++) {
        	listeCarte[i]= new Carte((int) scene.getWidth()-250,120+i*10*(grilleJeu.getTaille()+1),grilleJeu);
        	listeCarte[i].actualiserListeMove(grilleJeu);
        	root.getChildren().add(listeCarte[i]);
        }
        zoneScore.setFill(Color.BLACK);
        zoneScore.setFont(fontScore);
        gameOver= new Text("");//message perdu
		gameOver.setFill(Color.TRANSPARENT);
		gameOver.setFont(font);
		gameOver.setX(scene.getWidth()/2);
		gameOver.setY(scene.getHeight()/2);
		root.getChildren().add(gameOver);
		root.getChildren().add(imageBonus);
        root.getChildren().add(zoneScore);
        root.getChildren().add(grilleJeu);
        //jouer musique
        /*final Media media = new Media("file://cell/Valance.mp3");
    final MediaPlayer mediaPlayer = new MediaPlayer(media);
    MediaView mediaView = new MediaView(mediaPlayer);
        mediaPlayer.play();*/
        //tools bar de débuggage
        Button reset = new Button("New Game");//dit se que fait le bouton
        reset.setFocusTraversable(false);
        reset.setOnAction(value ->  { // action du bouton reset
        	try {
				resetPartie(tailleTableau,nbrCarte,nbrPop,debug);
			} catch (Exception e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
         });
        // creation zone d'options
        Button option = new Button("Options");//dit se que fait le bouton
        option.setFocusTraversable(false);
        option.setOnAction(value ->  { // action du bouton option
        	Group groupeOption = new Group();
            Scene sceneOption = new Scene(groupeOption, scene.getWidth(), scene.getHeight(), Color.LIGHTGREY); // la fenetre window
            fondOption.setFitWidth(sceneOption.getWidth()); // on met en pleine fenetre l'image de fond
            fondOption.setFitHeight(sceneOption.getHeight()); 
            groupeOption.getChildren().add(fondOption); 
            Text titreOption= new Text("Option du jeu");
            titreOption.setFont(new Font(40));
            titreOption.setLayoutX(20);
            titreOption.setLayoutY(80);
            titreOption.setFill(Color.WHITE);
            groupeOption.getChildren().add(titreOption);
            Text titreSliderT= new Text("Taille de la grille");
            titreSliderT.setFont(new Font(25));
            titreSliderT.setLayoutX(30);
            titreSliderT.setLayoutY(130);
            titreSliderT.setFill(Color.WHITE);
            groupeOption.getChildren().add(titreSliderT);
            Slider sliderTaille = new Slider(); // slider pour choisir taille grille
            Text sliderInfoT = new Text();
            sliderTaille.setMin(2);
            sliderTaille.setMax(MAXGRILLE);
            sliderTaille.setValue(tailleTableau);
            sliderTaille.setShowTickLabels(false);
            sliderTaille.setShowTickMarks(false);
            sliderTaille.setMajorTickUnit(1);
            sliderTaille.setMinorTickCount(0);
            sliderTaille.setBlockIncrement(1);
            sliderTaille.setLayoutX(50);
            sliderTaille.setLayoutY(145);
            sliderInfoT.setLayoutX(200);
            sliderInfoT.setLayoutY(160);
            sliderInfoT.setFont(new Font(20));
            sliderInfoT.setFill(Color.WHITE);
            sliderInfoT.setText(""+Math.round(sliderTaille.getValue()));
            groupeOption.getChildren().add(sliderTaille);
            groupeOption.getChildren().add(sliderInfoT);
            
            Slider sliderPop = new Slider(); // slider pour choisir nbr nouvelles case dans la grille
            Text sliderInfoP = new Text(); // texte de la valeur du slide
            sliderPop.setMin(1);
            sliderPop.setMax(Math.pow(Math.round(sliderTaille.getValue()),2));
            sliderPop.setValue(nbrPop);
            sliderPop.setShowTickLabels(false);
            sliderPop.setShowTickMarks(false);
            sliderPop.setMajorTickUnit(1);
            sliderPop.setMinorTickCount(0);
            sliderPop.setBlockIncrement(1);
            sliderPop.setLayoutX(50);
            sliderPop.setLayoutY(200);
            sliderInfoP.setLayoutX(200);
            sliderInfoP.setLayoutY(215);
            sliderInfoP.setFont(new Font(20));
            sliderInfoP.setFill(Color.WHITE);
            sliderInfoP.setText(""+Math.round(sliderPop.getValue()));
            groupeOption.getChildren().add(sliderPop);
            groupeOption.getChildren().add(sliderInfoP);
            Text titreSliderP= new Text("Nombre de nouvelles cases à chaque tour");
            titreSliderP.setFont(new Font(25));
            titreSliderP.setLayoutX(30);
            titreSliderP.setLayoutY(190);
            titreSliderP.setFill(Color.WHITE);
            groupeOption.getChildren().add(titreSliderP);
            sliderTaille.valueProperty().addListener(Event -> {
            	sliderInfoT.setText(""+Math.round(sliderTaille.getValue()));
            	sliderPop.setMax(Math.pow(Math.round(sliderTaille.getValue()),2));
            });
            sliderPop.valueProperty().addListener(Event -> {
            	sliderInfoP.setText(""+Math.round(sliderPop.getValue()));
            });
            CheckBox debuggage = new CheckBox("Afficher la valeur des cases");
            debuggage.setSelected(debug);
            debuggage.setLayoutX(50);
            debuggage.setLayoutY(220);
            groupeOption.getChildren().add(debuggage);
            debuggage.setTextFill(Color.WHITE);
            Button boutonJouer = new Button("Appliquer");//dit se que fait le bouton
            boutonJouer.setFocusTraversable(false); // creation bouton pour revenir jouer
            boutonJouer.setOnAction(Event ->  {
            	primaryStage.setScene(scene);
            	try {
					resetPartie((int)Math.round(sliderTaille.getValue()),nbrCarte,(int)Math.round(sliderPop.getValue()),debug=debuggage.isSelected()); // on fais une nouvelle partie avec les nouveaux parametre + on met debug 
				} catch (Exception e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
            }); // action du bouton jouer
            Button boutonReturn = new Button("Retour");//dit se que fait le bouton
            boutonReturn.setFocusTraversable(false); // creation bouton pour revenir jouer
            boutonReturn.setOnAction(Event ->  {
            	primaryStage.setScene(scene);
            }); // action du bouton jouer
            primaryStage.setScene(sceneOption);
            ToolBar toolOption = new ToolBar(
            		boutonJouer,
            		boutonReturn
            		);
            toolOption.setMinWidth(sceneOption.getWidth()); // on set la longueur de la barre au max de la largeur
            groupeOption.getChildren().add(toolOption);
            toolOption.setMinWidth(sceneOption.getWidth()); // on set la longueur de la barre au max de la largeur
       	 	fondOption.setFitWidth(sceneOption.getWidth()); // on met en pleine fenetre l'image de fond
       	 	fondOption.setFitHeight(sceneOption.getHeight()); 
            sceneOption.widthProperty().addListener((obs, oldVal, newVal) -> {
            	 toolOption.setMinWidth(sceneOption.getWidth()); // on set la longueur de la barre au max de la largeur
            	 fondOption.setFitWidth(sceneOption.getWidth()); // on met en pleine fenetre l'image de fond
            });
            sceneOption.widthProperty().addListener((obs, oldVal, newVal) -> {
            	fondOption.setFitHeight(sceneOption.getHeight()); 
            });
         });
        // sortie zone d'options
        
        toolBar = new ToolBar( // on ajoute la barre d'outils avec ses options
        		 reset,
        		 option,
        	     new Separator(),
        	     zoneScore
        	 );
        toolBar.setMinWidth(scene.getWidth());
	    
        root.getChildren().add(toolBar);
        // keylistener = on check les touches enfonc�es
        scene.setOnKeyPressed(new EventHandler<KeyEvent>() { // on active les touches si elles sont activ� et on casse le switch
            @Override
            public void handle(KeyEvent event) {
                switch (event.getCode()) {
                    case UP:    haut = true; break;
                    case DOWN:  bas = true; break;
                    case LEFT:  gauche  = true; break;
                    case RIGHT: droite  = true; break;
				default:
					break;
                }
            }
        });

        scene.setOnKeyReleased(new EventHandler<KeyEvent>() { // on d�sactive les touches si elles ne sont plus activ� et on casse le switch
            @Override
            public void handle(KeyEvent event) {
                switch (event.getCode()) {
                    case UP:    haut = false; break;
                    case DOWN:  bas = false; break;
                    case LEFT:  gauche  = false; break;
                    case RIGHT: droite  = false; break;
				default:
					break;
                }
            }
        });
        primaryStage.setScene(scene);
        primaryStage.show();
        gameOver.toFront();
        AnimationTimer timer = new AnimationTimer() {
            @Override
            public void handle(long now) {//main du jeu /boucle de jeu dans la fenetre
            	try {
            		// Toutes les fonctions pour actualiser la situation
	                
	                if(grilleJeu.getAnimationGroupe().getStatus()== Status.RUNNING){ // on bloque le temps pour jouer l'animation
	                	if(debug)
	                		System.out.println("animation en cours");
					}else if(grilleJeu.getFileAnimation().size()>0 && grilleJeu.getAnimationGroupe().getStatus()!= Status.RUNNING ) { // on lance l'animation
	                	grilleJeu.jouerAnimationSeq(nbrPop);
	                }else if(grilleJeu.tablePlein()&&grilleJeu.perdu() ) { // ecran de game over
	                	zoneScore.setText(actualiserScore());
						gameOver.setText("Vous avez Perdu\nScore : "+grilleJeu.getScore());
						gameOver.setFill(Color.WHITE);
						gameOver.setX(scene.getWidth()/2-300);
						gameOver.setY(scene.getHeight()/2);
						gameOver.toFront();
					}
					else if(grilleJeu.gagner()) {
						zoneScore.setText(actualiserScore());
						gameOver.setText("Gagné !\nScore : "+grilleJeu.getScore());
						gameOver.setFill(Color.WHITE);
						gameOver.setX(scene.getWidth()/2-200);
						gameOver.setY(scene.getHeight()/2);
						gameOver.toFront();
					}
					else  {
						//Quand le jeu attend un ordre
						grilleJeu.actualiserPosition();
			        	zoneScore.setText(actualiserScore());
						try { // selon la fleche press� on bougera dans un sens le jeu
							move=false;
					        if(haut) {
					        	haut=false;
					        	if(grilleJeu.testMonter()) {
					        		grilleJeu.haut();
						        	move=true;
					        	}
					        }
					        if(bas) {
					        	bas=false;
					        	if(grilleJeu.testDescendre()) {
					        		grilleJeu.bas();
						        	move=true;
					        	}
					        }
					        if(gauche) {
					        	gauche=false;
					        	if(grilleJeu.testGauche()) {
					        		grilleJeu.gauche();
						        	move=true;
					        	}
					        }
					        if(droite) {
					        	droite=false;
					        	if(grilleJeu.testDroite()) {
					        		grilleJeu.droite();
					        		move=true;
					        	}
					        }
					        if(move) {
					        	//realiserTour();
					        	grilleJeu.actualiserPosition();
					        	zoneScore.setText(actualiserScore());
					        }
						} catch (Exception e) {
							// TODO Auto-generated catch block
							e.printStackTrace();
						}
					}
				} catch (Exception e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
			};
        };
		timer.start();
    }
    public void actualiserAffichage(Grille grilleJeu) {
    	toolBar.setMinWidth(scene.getWidth()); // on set la longueur de la barre au max de la largeur
    	imageView.setFitWidth(scene.getWidth()); // on met en pleine fenetre l'image de fond
        imageView.setFitHeight(scene.getHeight());
        grilleJeu.setEchelle(Math.min(scene.getWidth()-400,scene.getHeight()-200)/500*(double)(4.0/tailleTableau));
        grilleJeu.actualiserAffichage();
        for(int i=0;i<nbrCarte;i++) {
        	listeCarte[i].actualiserAffichage((int) scene.getWidth()-250,120+i*10*(grilleJeu.getTaille()+1));
        }
        imageBonus.setX((int) scene.getWidth()-250);
    }
    public void realiserTour() throws Exception {
    	zoneScore.setText(actualiserScore());
    	grilleJeu.realiserTour();
    }
    public String actualiserScore() {
    	return "Score : "+grilleJeu.getScore();
    }
	public Grille getGrilleJeu() {
		return grilleJeu;
	}
	public Group getRoot() {
		return root;
	}
	public void resetPartie(int tailleTableau, int nbrCarte,int nbrPop, boolean debug) throws Exception { // permet aux parametres de s'appliquer
		this.nbrPop=nbrPop;
		this.tailleTableau=tailleTableau;
		this.nbrCarte=nbrCarte;
		actualiserAffichage(grilleJeu);
		gameOver.setFill(Color.TRANSPARENT);
		gameOver.setText("");
		grilleJeu.reset();
		zoneScore.setText(actualiserScore());
		root.getChildren().remove(grilleJeu);
		grilleJeu = new Grille(50, 50,Math.min(scene.getWidth()-400,scene.getHeight()-200)/500*(double)(4.0/tailleTableau),tailleTableau,debug); // position de la grille
		grilleJeu.reset();
		root.getChildren().add(grilleJeu);
		for(int i=0;i<nbrCarte;i++) {
			root.getChildren().remove(listeCarte[i]);
        	listeCarte[i]= new Carte((int) scene.getWidth()-250,120+i*10*(grilleJeu.getTaille()+1),grilleJeu);
        	listeCarte[i].actualiserListeMove(grilleJeu);
        	root.getChildren().add(listeCarte[i]);
        }
	}
}