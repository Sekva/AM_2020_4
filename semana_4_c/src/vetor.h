#ifndef VETOR_H
#define VETOR_H

typedef struct {
  double* d;
  unsigned int tamanho;
} Vetor;

Vetor* novo_vetor(unsigned int tamanho);
unsigned int tamanho(Vetor *v);
double produto_interno(Vetor* a, Vetor* b);
void limpar_vetor(Vetor* v);
void printar_vetor(Vetor* v);

#endif
