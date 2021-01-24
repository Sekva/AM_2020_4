#ifndef DADOS_H
#define DADOS_H

typedef struct {
  double** x;
  unsigned int d;
  unsigned char* y;
  unsigned long n_dados;
} Dados;

Dados *carregar_iris();
Dados *carregar_wine();
#endif
