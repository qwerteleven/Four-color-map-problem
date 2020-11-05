int : node_count;
set of int: nodes = 1..node_count;

int : aristas_count;

array [nodes] of var nodes: colores;
array [nodes] of set of nodes: map;

constraint forall(i in nodes)(card({colores[i]} intersect map[i]) = 0);
constraint forall(i in nodes)(forall(j in map[i] where j != i)(colores[i] != colores[j]));
constraint forall(i in nodes)(forall(j in map[i] where j != i)(colores[j] != colores[i]));

solve minimize max(colores);
