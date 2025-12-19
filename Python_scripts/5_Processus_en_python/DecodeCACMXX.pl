#
# Auteurs: Livio Dadone, Gabriel Bragança De Oliveira
# Nom du fichier: DecodeCACMXX.pl
# Objectif du programme:
#   Décoder les fichiers CACM au format original et produire des fichiers texte intermédiaires exploitables
#   pour les étapes suivantes de nettoyage et de filtrage.
#
use strict;
use warnings;
use utf8;

use FindBin qw($Bin);
use File::Spec;
use File::Path qw(make_path);

my $BASE_DIR = File::Spec->catdir($Bin, '..', '..');
my $COL_DIR  = File::Spec->catdir($BASE_DIR, 'Collection');

if (!-d $COL_DIR) {
    make_path($COL_DIR) or die "Erreur: impossible de créer le dossier Collection: $COL_DIR\n";
}

my $CACM_ALL = File::Spec->catfile($Bin, 'cacm.all');
open(my $F, '<', $CACM_ALL) or die "Erreur d'ouverture du fichier $CACM_ALL\n";

my $collection_list = File::Spec->catfile($COL_DIR, 'Collection');
open(my $COL, '>', $collection_list) or die "Erreur de creation de Collection\n";

my $str  = "";
my $Num  = 0;
my $Go   = 0;
my $Path = $COL_DIR;

my $NF;

while (!eof($F)) {

    if ($str =~ /\.I\s/) {
        close($NF) if defined $NF;
        $str =~ s/\.I\s//g;
        $Num = $str;
        print $COL "CACM-$Num\n";
        print "Processing ... CACM-$Num\n";
        my $out_doc = File::Spec->catfile($Path, "CACM-$Num");
        open($NF, '>', $out_doc) or die "Erreur d'ouverture/creation du fichier $out_doc\n";
    }

    if (($str =~ /\.T/) || ($str =~ /\.A/) || ($str =~ /\.W/) || ($str =~ /\.B/)) {
        $Go = 1;
        while ($Go == 1) {
            my $line = <$F>;
            last unless defined $line;
            chomp($line);
            $str = $line;

            if (($str eq ".W") || ($str eq ".B") || ($str eq ".N") || ($str eq ".A") ||
                ($str eq ".X") || ($str eq ".K") || ($str eq ".T") || ($str eq ".I")) {
                $Go = 0;
                last;
            } else {
                print $NF "$str " if defined $NF;
            }
        }
    } else {
        my $line = <$F>;
        last unless defined $line;
        chomp($line);
        $str = $line;
    }
}

close($NF) if defined $NF;
close($COL);
close($F);
