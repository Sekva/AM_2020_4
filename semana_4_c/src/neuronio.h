#include "vetor.h"

#ifndef NEURONIO_H
#define NEURONIO_H

typedef struct {
  Vetor* w; 
} Neuronio;

Neuronio* novo_neuronio(unsigned int tamanho);
double aplicar_neurorio(Vetor *entrada, Neuronio *neuronio );
void limpar_neuronio(Neuronio* n);
void printar_neuronio(Neuronio* n);

#endif
