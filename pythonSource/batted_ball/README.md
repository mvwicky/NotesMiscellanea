<script type="text/javascript" src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-MML-AM_CHTML"></script>

# Batted Ball Python Scripts

<h3> Exit Angles: \( \phi \) and \( \theta \) </h3>
<div class="column">
    \( \theta  \) (theta): angle from horizontal <br />
    \( \phi \) (phi): angle from straight away center <br />
    \( \phi (CF) = \frac{\pi}{4} \) <br />
    \( \hspace{2em} \) 1st Base Line:\( \phi = 0\) <br />
    \( \hspace{2em} \) 3rd Base Line: \( \phi  = \frac{\pi}{2} \) <br />
    \( \hspace{2em} \) if \( \phi < 0 \) or \( \phi > \frac{\pi}{2} \): ball is foul <br />
    <br />
    <h3> Calculating Drag Due to Air Resistance </h3>
    \( m = 0.145kg \): mass of a baseball <br />
    \( r = 73mm = 73\cdot 10^{-3}m \): radius of a baseball <br />
    \( A = \pi\cdot r^2 \): frontal area of a baseball <br />
    \( C_D = 0.3 \): coefficient of drag [<a href="http://www.grc.nasa.gov/www/k-12/airplane/balldrag.html">ref</a>] <br />
    \( p_o = 101.325\cdot 10^3 Pa \): sea level standard atmospheric pressure <br />
    \( L = 0.0065 \frac{K}{m} \): temperature lapse rate <br />
    \( T_o = 288.15 K \): sea level standard temperature <br />
    \( R = 8.31447 \frac{J}{mol\cdot K} \): ideal gas constant <br />
    \( M = 0.0289644 \frac{kg}{mol} \): molar mass of air <br />
    \( g = 9.80665 \frac{m}{s^2} \): acceleration due to gravity <br />
    \( h \): altitude in meters <br />
    \( p = p_o\cdot (1 - \frac{L\cdot h}{T_o})^{\frac{g\cdot M}{R\cdot L}} Pa \): absolute pressure at height, \( h \) <br />
    \( T = T_o - L\cdot h \): absolute temperature at height, \( h \) <br />
    \( \rho = \frac{p\cdot M}{R\cdot T} \): air density <br />
    \( k = \frac{1}{2}\cdot\rho\cdot A\cdot C_D \): drag factor <br />
    <h3> Calculating Velocity and Distance Traveled </h3>
    \( \mathbf{\vec{v}} \): total velocity vector <br />
    \( v_x(t) \): horizontal velocity <br />
    \( \hspace{2em} v_x(0) = \vec{v}\cdot\cos(\phi)\cdot\sin(90-\theta) \): initial velocity in the \( x \) direction <br />
    \( \hspace{2em} v_x(t) = \frac{1}{\frac{1}{v_x(0)} + \frac{k\cdot t}{m}} = v_x(0)^{-1} + (\frac{k\cdot t}{m})^{-2} \) <br />
    \( \hspace{2em} v_y(0) = \vec{v}\cdot\sin(\phi)\cdot\cos(90-\theta) \): initial velocity in the \( y \) direction <br />
    \( \hspace{2em} v_y(t) = v_x(t) \): with different exit angles <br />
    \( \hspace{2em} s_x(t), s_y(t) \): horizontal distance traveled (integrations of velocity) <br />
    \( \hspace{2em} s_{x,y}(t) = \frac{m}{k}\cdot(\ln(\frac{k\cdot t\cdot v_{x,y}(0)+m}{m})) \) <br />
    \( v_z(t) \): vertical velocity <br />
    \( \hspace{2em} v_z(0) = \cos(90 - \theta) \) <br />
    \( \hspace{2em} v_z(t) \): different depending on ascending or descending <br />
    <a href="https://en.wikipedia.org/wiki/Trajectory_of_a_projectile#Trajectory_of_a_projectile_with_air_resistance">ref</a><br />
</div>