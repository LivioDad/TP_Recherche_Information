#
# Auteurs: Livio Dadone, Gabriel Bragança De Oliveira
# Nom du fichier: remove.pl
# Objectif du programme:
#   Filtrer le contenu nettoyé afin de supprimer les mots vides (stop words)
#   et produire des fichiers texte prêts pour l’analyse lexicale.
#


##AMC
##remove.pl
# Écrire une fonction qui ouvre les fichiers CACM-XX.flt un à un 
# et qui applique le stop-list common-words en enlevant tous les termes de ces fichiers qui y apparaissent. 

# Le résultat du filtrage sera mis dans un fichier portant le même nom 
# que ces fichiers avec une nouvelle extension .stp

# Indication: On pourra utiliser une table de hash en parcourant le fichier common-words 
# et en associant à chaque terme de fichier pris comme une clé de la table, la valeur 1. 
# Le filtrage se fera en regardant si un terme des fichiers CACM-XX.flt est une clé de cette table de hash ou non. 

use FindBin qw($Bin);
use File::Spec;

my $COLLECTION_DIR = File::Spec->catdir($Bin, '..', '..', 'Collection');
my $OUTPUTS_DIR    = File::Spec->catdir($Bin, '..', '..', 'outputs');

my $STOP_FILE = "$COLLECTION_DIR/common_words";
if (!-f $STOP_FILE) {
	$STOP_FILE = "$OUTPUTS_DIR/common_words";
}

my %swords;
open(STOPW,$STOP_FILE) || die ("Erreur d'ouverture du fichier de fichierAlire") ;
while (<STOPW>) {
	$_ =~ s/\n//g;
	$swords{$_}=1;
}

while ( my ($cle,$val)=each(%swords) ) {
		 print "motvide: $cle, value: $val\n";
		
}

open(COLL,"<$COLLECTION_DIR/Collection") || die ("Erreur d'ouverture du fichier de fichierAlire") ;
while (<COLL>) {
	$_ =~ s/\n//g;
	$fic = $_;
	
	open(F,"<$COLLECTION_DIR/$fic.flt") || die ("Erreur d'ouverture du fichier de fichierALire") ;
	open(STP,">$COLLECTION_DIR/$fic.stp") || die ("Erreur d'ouverture du fichier de fichierAEcrire") ;

	while (<F>) {
		$_ =~ s/\n//g;
		$_ =~ s/\s+/ /;
	 
	@tab=split(/ /,$_);
	$nbvide = 0;
	foreach my $v (@tab) {
		if (!$swords{$v}) {
			print STP $v . " ";
		}
		else { $nbvide++; print "(**". $v . " ";}
	}
	print $fic . " " . $nbvide . "\n";

	}
	close(F);
	close(STP);
 }
 close(COLL);
