"""
zipf_plot.py

Lit le fichier outputs/counter.txt (rang, fréquence, mot)
et génère un graphique log-log (loi de Zipf) dans outputs/zipf_plot.png.

Fonctionnalités :
- Lecture du mot (3ᵉ colonne) en plus du rang et de la fréquence
- Vérifications basiques sur les données
- Régression linéaire sur les données log-log pour estimer l'exposant de Zipf
- Sélection de quelques mots répartis sur tous les rangs (en échelle log)
- Annotation lisible : offsets alternés, petites flèches, contour blanc du texte
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import numpy as np
from itertools import cycle


# Répertoires
SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPT_DIR.parent
COUNTER_FILE = BASE_DIR / "outputs" / "counter.txt"
OUTPUT_PNG = BASE_DIR / "outputs" / "zipf_plot.png"


@dataclass
class WordStat:
    """Représente une ligne de counter.txt."""
    rank: int
    freq: int
    word: str


def lire_counter(path: Path) -> List[WordStat]:
    """
    Lit le fichier counter.txt et renvoie une liste de WordStat.

    On suppose un format par ligne :
        rang freq mot
    où 'mot' peut éventuellement contenir des espaces (on recolle tout après la 2ᵉ colonne).

    Les lignes non parseables (en-têtes, vides, etc.) sont ignorées.
    """
    stats: List[WordStat] = []

    if not path.exists():
        raise FileNotFoundError(f"Fichier introuvable : {path}")

    with path.open(encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line:
                continue

            parts = line.split()
            if len(parts) < 3:
                continue

            try:
                rank = int(parts[0])
                freq = int(parts[1])
            except ValueError:
                # Probable ligne d'en-tête ou format invalide
                continue

            word = " ".join(parts[2:])
            stats.append(WordStat(rank=rank, freq=freq, word=word))

    # On s'assure que les données sont triées par rang croissant
    stats.sort(key=lambda s: s.rank)
    return stats


def extraire_rang_freq(stats: List[WordStat]) -> Tuple[np.ndarray, np.ndarray]:
    """
    À partir d'une liste de WordStat, construit deux tableaux NumPy :
    - ranks : rangs
    - freqs : fréquences
    """
    ranks = np.array([s.rank for s in stats], dtype=float)
    freqs = np.array([s.freq for s in stats], dtype=float)
    return ranks, freqs


def choisir_indices_a_annoter(stats: List[WordStat], nb_labels: int = 10) -> List[int]:
    """
    Choisit quelques indices de mots à annoter, répartis sur l'échelle
    des rangs en LOG10 pour éviter qu'ils ne soient concentrés dans la queue.

    - stats : liste de WordStat triée par rang
    - nb_labels : nombre maximal de mots à annoter
    """
    n = len(stats)
    if n == 0:
        return []

    nb_labels = min(nb_labels, n)

    ranks = np.array([s.rank for s in stats], dtype=float)
    log_ranks = np.log10(ranks)

    # On choisit des positions cibles régulièrement espacées en log10
    targets = np.linspace(log_ranks.min(), log_ranks.max(), nb_labels)

    indices = []
    for t in targets:
        idx = int(np.argmin(np.abs(log_ranks - t)))
        indices.append(idx)

    # On enlève les doublons, puis on trie
    indices = sorted(set(indices))
    return indices


def annoter_mots_no_overlap(ax, stats: List[WordStat], indices: List[int]) -> None:
    """
    Annote des mots avec des offsets alternés pour améliorer la lisibilité,
    en ajoutant des petites flèches reliant le texte au point.

    - ax : axes matplotlib courants
    - stats : liste de WordStat triée
    - indices : indices des mots à annoter dans stats
    """
    # Offsets alternés (en pixels) pour éviter le chevauchement
    offsets = cycle([
        (8, 8), (8, -8),
        (-8, 8), (-8, -8),
        (12, 0), (-12, 0),
        (0, 12), (0, -12),
    ])

    for idx in indices:
        s = stats[idx]
        dx, dy = next(offsets)

        txt = ax.annotate(
            s.word,
            xy=(s.rank, s.freq),
            xytext=(dx, dy),
            textcoords="offset points",
            fontsize=8,
            ha="left",
            va="bottom",
            arrowprops=dict(
                arrowstyle="-",
                lw=0.6,
                alpha=0.6,
            ),
        )

        # Contour blanc pour garder le texte lisible sur les points/traits
        txt.set_path_effects([
            pe.withStroke(linewidth=2, foreground="white")
        ])


def tracer_zipf(ranks: np.ndarray,
                freqs: np.ndarray,
                stats: List[WordStat],
                nb_labels: int = 10) -> None:
    """
    Trace le graphique log-log (loi de Zipf) et annote quelques mots sélectionnés.

    - ranks, freqs : tableaux de même taille
    - stats : liste de WordStat correspondant (même ordre)
    - nb_labels : nombre maximal de mots à annoter
    """
    if ranks.size == 0 or freqs.size == 0:
        raise ValueError("Aucune donnée à tracer (ranks ou freqs vide).")

    plt.figure(figsize=(8, 6))

    # Nuage de points en échelle log-log
    plt.loglog(ranks, freqs, ".", alpha=0.5)

    # Régression linéaire sur log10(rang) et log10(freq),
    # en ignorant éventuellement les tout premiers et tout derniers rangs
    log_r = np.log10(ranks)
    log_f = np.log10(freqs)

    # Petit filtrage pour exclure les extrêmes (optionnel mais souvent plus propre)
    # Ici on garde les rangs entre 5 et 5000 si possible
    mask = (ranks >= 5) & (ranks <= 5000)
    mask &= np.isfinite(log_r) & np.isfinite(log_f)

    if mask.sum() > 2:
        slope, intercept = np.polyfit(log_r[mask], log_f[mask], 1)

        # Ligne de tendance
        log_r_sorted = np.linspace(log_r[mask].min(), log_r[mask].max(), 200)
        log_f_fit = slope * log_r_sorted + intercept
        plt.plot(10 ** log_r_sorted, 10 ** log_f_fit, linewidth=1)

        zipf_exponent = -slope
        title = f"Loi de Zipf - Collection CACM (exposant ≈ {zipf_exponent:.2f})"
    else:
        title = "Loi de Zipf - Collection CACM"

    ax = plt.gca()

    # Choix des indices à annoter (répartis en log-rang)
    indices = choisir_indices_a_annoter(stats, nb_labels=nb_labels)

    # Met en évidence les points sélectionnés
    for i in indices:
        s = stats[i]
        ax.scatter(s.rank, s.freq)

    # Ajoute les annotations lisibles
    annoter_mots_no_overlap(ax, stats, indices)

    # Axes / labels
    plt.xlabel("Rang (log)")
    plt.ylabel("Fréquence (log)")
    plt.title(title)
    plt.grid(True, which="both", linestyle=":", alpha=0.4)

    plt.tight_layout()


def main() -> None:
    try:
        stats = lire_counter(COUNTER_FILE)
    except FileNotFoundError as e:
        print(f"[ERREUR] {e}")
        return

    if not stats:
        print("[ERREUR] Aucune donnée valide lue depuis counter.txt")
        return

    ranks, freqs = extraire_rang_freq(stats)

    if ranks.shape != freqs.shape:
        print("[ERREUR] ranks et freqs n'ont pas la même taille.")
        print(f"  ranks: {ranks.shape}, freqs: {freqs.shape}")
        return

    # Trace le graphe et annote quelques mots
    tracer_zipf(ranks, freqs, stats, nb_labels=10)

    # Sauvegarde
    OUTPUT_PNG.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUTPUT_PNG, dpi=300)
    print(f"[OK] Figure sauvegardée dans : {OUTPUT_PNG}")

    # Affichage à l'écran pour inspection
    plt.show()

    # Petit résumé console (utile pour le rapport)
    print("\n[INFO] Rappel (loi de Zipf) :")
    print("      Dans un corpus de texte, la fréquence d'un mot est approximativement")
    print("      inversement proportionnelle à son rang : f(r) ≈ C / r^s.")
    print("      Un graphique log-log donne donc (en première approximation) une droite.")
    print("      L'exposant s est l'opposé de la pente de cette droite.")


if __name__ == "__main__":
    main()
