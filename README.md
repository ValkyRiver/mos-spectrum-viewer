# ValkyRiver: MOS Spectrum Viewer
**MOS Spectrum Viewer** is a visualization for MOS (moment-of-symmetry) scales and where each equal temperament fits on its step ratio spectrum.

## MOS scales
**MOS scales** have the property that every step size other than the period must come in exactly two sizes. They are commonly denotes xL ys, where the L and s refer to the large and small step respectively. For a xL ys scale, the period is 1/GCD(x, y) of an octave (so if x and y are coprime, then the period will be a full octave).

As for exactly how big L and s are, the ratio between L and s is the **step ratio** or **hardness**. On one extreme, small step becomes so big that it equals the large step (**equalized**). On the other extreme, the small step goes to 0 (**collapsed**). The range between equalized and collapsed form the spectrum of that MOS — if L/s is rational (or ∞), then there will be an equal temperament with a MOS scale of hardness L:s.

Each MOS has two **generator** intervals where repeatedly stacking it will produce all notes of the scale, modulo period. These two generators are period-inversions of each other. The size of the generator is correlated with the L:s ratio, so the generator can only be in a particular range — the two extremes produce the equalized and collapsed scale.

Once the notes of the MOS have been found, one can also choose which note to start the scale on — these are the **modes** of the MOS. In this visualizer, they are ordered by the number of generators stacked — specifically, the first mode is always the mode with the most number of s steps closer to the start of the scale. A xL ys MOS has (x + y)/GCD(x, y) modes.

For example, the diatonic scale, 5L 2s, has seven modes: sLLsLLL (locrian), sLLLsLL (phrygian), LsLLsLL (minor/aeolian), LsLLLsL (dorian), LLsLLsL (mixolydian), LLsLLLs (major/ionian), and LLLsLLs (lydian). The octatonic/diminished/tetrawood scale, 4L 4s, only has two modes: sLsLsLsL and LsLsLsLs (since the period is 1/4 of an octave).

## The graph
On the graph, the horizontal axis on the top represents the size of the generator interval. For specific values of the generator size, L:s ends up being rational, meaning that there is an equal temperament — these are labeled on the bottom. Note that if an equal temperament contains a particular MOS with a particular hardness, then so will all of its multiples, which are labeled in green.

For larger equal divisions, it may be possible to have two or more intervals within the generator range. This means that the equal temperament has more than one subset of pitches that form a particular MOS. In this case, the one with the flatter generator is labeled "b", and the one with the sharper generator is labeled "#". (If there are three or more, the middle ones are labeled "~" — I have yet to implement a system for distinguishing between four or more). Note that the "b" and "#" labels will flip if the generator is inverted.

Each of the equal temperaments will have a vertical line on the graph. Each point on the vertical line corresponds to one interval in that equal temperament — the vertical axis on the left shows the size of the interval. Only the lowest equal temperament with a particular hardness of the MOS will be plotted — multiples of the same MOS of the same hardness will not.

The slanted, colored horizontal lines indicate the pitch of each of the notes of the selected mode of the MOS in different parts of the spectrum. The edge where the lines are evenly spaced is the "equalized" side — the edge where several lines converge to a single point is the "collapsed" side.

## Relationships between MOSs
The **sister** is obtained by reversing the number of L and s steps. So the sister of xL ys is yL xs. This is the MOS you get if you try to push s to be bigger than L — you end up in the spectrum of the sister MOS. Therefore, a MOS shares its equalized extreme with its sister.

The **parent** of a MOS is obtained by merging all pairs of adjacent L and s steps into an even bigger step. For a MOS xL ys, the parent will be min(x, y)L |x−y|s. If x = y, then the parent of xL ys ends up being an equal temperament with x steps.

Each MOS has two **daughters** — they are obtained by splitting a L step into a s step + another step (which I'll call c). Which one becomes the new L vs the new s step depends on the relative size of c and s. For a MOS xL ys, if c ≥ s, then the resulting daughter will be xL (x+y)s. If c ≤ s, then the resulting daughter is (x+y)L xs. The two daughters will be sisters of each other, and c = s is their common "equalized" extreme.

There is also **neutralization** — this is obtained by replacing pairs of L and s (not necessarily adjacent) steps with a neutral step n, where n = (L+s)/2. With the right choice of pairs, a new MOS is obtained — for a MOS xL ys, if x > y, then the MOS neutralizes to (x−y)L 2ys. If x < y, then the result is 2xL (y−x)s. And if x = y, the result is an equal temperament with x + y steps.

**README WIP**
