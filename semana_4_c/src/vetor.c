#include "vetor.h"
#include <stdlib.h>
#include <stdio.h>

Vetor *novo_vetor(unsigned int tamanho) {

  Vetor* v = malloc(sizeof(Vetor));

  v->tamanho = tamanho;
  v->d = calloc(tamanho, sizeof(double));

  
  return v;
}


double produto_interno(Vetor *a, Vetor *b) {


  unsigned int menor = 0;

  if(a->tamanho < b->tamanho) {
    menor = a->tamanho;
  } else {
    menor = b->tamanho;
  }

  int soma = 0;

  for(int i = 0; i < menor; i++) {
    soma += a->d[i] * b->d[i];
  }
  
  return soma;
  
}

void limpar_vetor(Vetor *v) {
  free(v->d);
  free(v);
}



void printar_vetor(Vetor *v) {
  printf("[");

  char p = 0;

  
  for(int i = 0; i < v->tamanho; i++) {

    if(!p) {
      printf("%f", v->d[i]);
      p = 1;
    } else {
      printf(", %f", v->d[i]);
    }
  }
  printf("]\n");
}
