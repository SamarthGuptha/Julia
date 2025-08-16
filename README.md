# Julia
Turn poems into beautiful fractals!

## How a Poem Becomes a Fractal
The transformation from text to a complex mathematical object happens in three main stages: in-depth analysis, mathematical mapping, and animated rendering.

### 1. Poem Analysis
First, the Python script performs a deep analysis of the source poem, extracting eight distinct numerical features. These features act as the poem's unique "fingerprint":

Textual Variety: Measures the diversity of letters used. A poem with a wide range of characters has a higher score.

Lexical Density: The ratio of unique words to total words. This represents the richness of the vocabulary.

Sentiment Compound: The overall emotional tone of the poem, calculated on a scale from -1.0 (very negative) to +1.0 (very positive).

Positivity: The proportion of words in the poem that have a positive connotation.

Average Word Length: The average number of letters per word, indicating the complexity of the language.

Average Line Length: The average number of words per line, representing the poem's rhythm and pacing.

Punctuation Density: The frequency of punctuation marks, which hints at the poem's structure and pauses.

Light/Dark Ratio: A thematic score based on the ratio of words associated with light and positivity versus those associated with darkness and negativity.

### 2. Mathematical Mapping
These abstract features are then used to define a dynamic path for the fractal's complex constant, c. A static fractal is defined by a single c, but an animation requires a moving c.

Finding a "Seed": The process starts with a base c value known to be in a visually interesting region of the complex plane (near the boundary of the Mandelbrot set).

Defining a Path: The poem's features are used to alter this seed and define a journey. For example, in the "Morphing" method:

The poem's sentiment and lexical density are used to calculate the animation's unique start point (c_start).

The light/dark ratio and positivity score define the animation's end point (c_end).

The Journey of c: The script calculates a straight line (or a circle) between these two poem-defined points. The animation is created by moving c along this path step-by-step.

### 3. Fractal Generation & Animation
For each step along the mathematical path, a complete Julia set fractal is rendered.

The script iterates from frame 0 to the NUM_FRAMES you set.

In each iteration, it calculates the new position of c along the path.

It then generates the full Julia set image for that specific c value.

This image is saved as a numbered frame (e.g., frame_000.png, frame_001.png, etc.).

When these frames are played in sequence, they create a smooth animation showing the fractal transforming as its underlying mathematical constant travels on a journey defined entirely by the source poem.
