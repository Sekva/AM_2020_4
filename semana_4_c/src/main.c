#include <stdio.h>
#include <stdlib.h>
#include "neuronio.h"
#include "dados.h"


Dados* base_dados_iris_completa;
Dados* base_dados_wine_completa;


void q_1_a() {

  

  
}


int main(int argc, const char** argv) {
  base_dados_iris_completa = carregar_iris();
  base_dados_wine_completa = carregar_wine();
  q_1_a();
  return 0;
}
