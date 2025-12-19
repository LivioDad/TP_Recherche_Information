#
# Auteurs: Livio Dadone, Gabriel Bragança De Oliveira
# Nom du fichier: clean.pl
# Objectif du programme:
#   Nettoyer les fichiers texte issus du décodage CACM en supprimant les balises inutiles
#   et en préparant les données pour l’étape de filtrage.
#

#!/usr/bin/perl
use strict;
use warnings;
use utf8;
use open ':std', ':encoding(UTF-8)';

use FindBin;
use File::Spec;

my $BASE_DIR       = File::Spec->catdir($FindBin::Bin, '..', '..');
my $COLLECTION_DIR = File::Spec->catdir($BASE_DIR, 'Collection');
my $LIST_FILE      = File::Spec->catfile($COLLECTION_DIR, 'Collection');

open(my $COLL, "<", $LIST_FILE)
  or die "Erreur d'ouverture du fichier liste: $LIST_FILE\n";

while (my $fic = <$COLL>) {
    chomp($fic);
    $fic =~ s/\r$//;          # important si le fichier est en CRLF
    next if $fic =~ /^\s*$/;  # saute les lignes vides

    my $in  = File::Spec->catfile($COLLECTION_DIR, $fic);
    my $out = File::Spec->catfile($COLLECTION_DIR, "$fic.flt");

    open(my $CACM, "<", $in)  or die "Erreur d'ouverture du fichier à lire: $in\n";
    open(my $F,    ">", $out) or die "Erreur d'ouverture du fichier à écrire: $out\n";

    while (my $line = <$CACM>) {
        $line =~ s/\n/ /g;
        $line =~ tr/àâäéèêëîïù/aaaeeeeiiu/;
        $line =~ s/(\"|\,|\=|\/|\.|\?|\'|\(|\)|\_|\$|\%|\+|\[|\]|\{|\}|\&|\;|\:|\~|\!|\@|\#|\^|\*|\||\<|\>|\-|\\s|\\)/ /g;
        $line =~ s/\s+/ /g;
        print $F lc($line);
    }

    close($CACM);
    close($F);
}

close($COLL);
