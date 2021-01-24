#include "neuronio.h"
#include <stdlib.h>

Neuronio *novo_neuronio(unsigned int tamanho) {
  Neuronio *n = malloc(sizeof(Neuronio));
  n->w = novo_vetor(tamanho);
  return n;
}

double aplicar_neurorio(Vetor *entrada, Neuronio *neuronio) {
  double v = produto_interno(neuronio->w, entrada);

  if (v > 0) {
    return 1;
  } else {
    return 0;
  }
}

void limpar_neuronio(Neuronio *n) {
  limpar_vetor(n->w);
  free(n);
}

void printar_neuronio(Neuronio *n) {
  printar_vetor(n->w);
}
