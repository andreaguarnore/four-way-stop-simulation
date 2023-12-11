# Four-way-stop-simulation

A simple simulation of a four-way stop in [Mesa](https://github.com/projectmesa/mesa).

## Jurisdiction modeled

All vehicles approaching the intersection are required to come to a full stop behind the stop line; then, when a driver arrives at the intersection:

- if no other vehicle is at another stop, or in the intersection, then the driver can proceed;

- otherwise, if there are vehicles at other stops, but none of which the driver has to give way to, and no other vehicle is in the intersection, then the driver can proceed;

- otherwise, wait for right-of-way.

## Implementation

The vehicles in the simulation move according to Nagel and Schreckenberg’s traffic model [1].

Deadlocks are solved arbitrarily, by giving highest priority to the northern group, second highest to the eastern group, and so on, in a clockwise manner.

## References

[1] Kai Nagel and Michael Schreckenberg. “A cellular automaton model for freeway traffic”. In: Journal de Physique I 2 (Dec. 1992), p. 2221. doi: 10.1051/jp1:1992277.

