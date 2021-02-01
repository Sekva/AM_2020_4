use rand::seq::SliceRandom;
use rand::thread_rng;
use std::{
    fs::File,
    io::{prelude::*, BufReader},
};

use std::collections::HashSet;

type DadoClassificado = (Vec<String>, String);

#[derive(Debug, PartialEq, Eq, Hash)]
pub enum No {
    Folha(String),
    Galho(usize, Vec<(String, No)>),
}

impl No {
    pub fn novo(base_dados: Vec<DadoClassificado>) -> No {
        let mut possiveis_valores_dos_atributos: Vec<Vec<String>> = Vec::new();
        for atributo in 0..base_dados[0].0.len() {
            let possiveis_valores_do_atributo: HashSet<String> = base_dados
                .iter()
                .map(|dado| dado.0[atributo].clone())
                .collect();
            possiveis_valores_dos_atributos
                .push(possiveis_valores_do_atributo.iter().cloned().collect());
        }

        No::criar_folha(
            base_dados,
            Vec::new(),
            possiveis_valores_dos_atributos.clone(),
        )
    }

    pub fn criar_folha(
        base_dados: Vec<DadoClassificado>,
        mut atributos_ignorados: Vec<usize>,
        possiveis_valores_dos_atributos: Vec<Vec<String>>,
    ) -> No {
        //caso que nao tenho certeza
        if base_dados.is_empty() {
            println!("base de dados vazia");
            panic!();
        }

        //parada da recursão
        let todas_classificacoes: Vec<String> = base_dados.iter().map(|e| e.1.clone()).collect();
        let possiveis_classificacoes: Vec<String> = todas_classificacoes.iter().cloned().collect();

        //usar possiveis_classificacoes SÓ com os atributos disponiveis
        if possiveis_classificacoes.len() == 1 {
            return No::Folha(possiveis_classificacoes.iter().nth(0).unwrap().clone());
        }

        //escolhe o atributo desse galho
        //lista de: (qual_atributo, quantos erros)
        let mut erros_dos_atributos: Vec<(usize, usize)> = Vec::new();
        for atributo in 0..base_dados[0].0.len() {
            if !atributos_ignorados.contains(&atributo) {
                let possiveis_valores_do_atributo =
                    possiveis_valores_dos_atributos[atributo].clone();

                let soma_dos_erros_dos_valores_desse_atributo: usize =
                    possiveis_valores_do_atributo
                        .iter()
                        .map(|possivel_valor| {
                            let linhas_com_o_possivel_valor_de_atributo: Vec<DadoClassificado> =
                                base_dados
                                    .iter()
                                    .filter(|e| &e.0[atributo] == possivel_valor)
                                    .cloned()
                                    .collect();

                            let mut numero_classificacoes: Vec<usize> = possiveis_classificacoes
                                .iter()
                                .map(|classificacao| {
                                    linhas_com_o_possivel_valor_de_atributo
                                        .iter()
                                        .filter(|e| &e.1 == classificacao)
                                        .count()
                                })
                                .collect();

                            numero_classificacoes.sort();
                            let mut erro_desse_valor_de_atributo = 0;

                            for n in numero_classificacoes.clone() {
                                erro_desse_valor_de_atributo += n;
                            }
                            erro_desse_valor_de_atributo -=
                                numero_classificacoes[numero_classificacoes.len() - 1];

                            erro_desse_valor_de_atributo
                        })
                        .sum();

                erros_dos_atributos.push((atributo, soma_dos_erros_dos_valores_desse_atributo));
            }
        }

        erros_dos_atributos.sort_by(|a, b| a.1.partial_cmp(&b.1).unwrap());

        //escolhe se vai ser um galho (com o atributo escolhido) ou folha

        //calcula os erros como folha

        let mut contagem_possiveis_classificacoes: Vec<(usize, String)> = possiveis_classificacoes
            .iter()
            .map(|classificacao| {
                (
                    base_dados
                        .iter()
                        .filter(|dado| &dado.1 == classificacao)
                        .count(),
                    classificacao.clone(),
                )
            })
            .collect();

        contagem_possiveis_classificacoes.sort_by(|a, b| a.0.partial_cmp(&b.0).unwrap());

        let mut erro_se_folha = 0;

        for cont in contagem_possiveis_classificacoes.clone() {
            erro_se_folha += cont.0;
        }

        erro_se_folha -=
            contagem_possiveis_classificacoes[contagem_possiveis_classificacoes.len() - 1].0;

        if erro_se_folha < erros_dos_atributos[0].1 {
            //entao é melhor ser uma folha
            //classifica como a classificacao com o menor erro
            let folha = No::Folha(contagem_possiveis_classificacoes[0].1.clone());
            println!("acabou melhor sendo folha: {:?}", folha);
            return folha;
        }

        //ok, ent vai ser um galho do atributo escolhido
        let atributo_escolhido = erros_dos_atributos[0].0;
        atributos_ignorados.push(atributo_escolhido);

        let possiveis_valores_do_atributo: Vec<String> =
            possiveis_valores_dos_atributos[atributo_escolhido].clone();

        //verificando se ja testou todos os dados do treino

        for valor in possiveis_valores_do_atributo.iter() {
            let base_dados_so_com_esse_valor_desse_atributo: Vec<DadoClassificado> = base_dados
                .iter()
                .filter(|el| &el.0[atributo_escolhido] == valor)
                .cloned()
                .collect();

            if base_dados_so_com_esse_valor_desse_atributo.is_empty() {
                let possiveis_classificacoes: HashSet<String> =
                    base_dados.iter().map(|dado| dado.1.clone()).collect();

                let mut lista_n_classificacoes: Vec<(usize, String)> = possiveis_classificacoes
                    .iter()
                    .map(|classificacao| {
                        (
                            base_dados
                                .iter()
                                .filter(|dado| &dado.1 == classificacao)
                                .count(),
                            classificacao.clone(),
                        )
                    })
                    .collect();

                lista_n_classificacoes.sort_by(|a, b| a.0.partial_cmp(&b.0).unwrap());
            }
        }

        // cada possivel valor do atributo vai apontar pra um nó

        let ramos_do_galho: Vec<(String, No)> = possiveis_valores_do_atributo
            .iter()
            .map(|valor| {
                let base_dados_so_com_esse_valor_desse_atributo: Vec<DadoClassificado> = base_dados
                    .iter()
                    .filter(|el| &el.0[atributo_escolhido] == valor)
                    .cloned()
                    .collect();

                let no: No;
                if base_dados_so_com_esse_valor_desse_atributo.is_empty() {
                    let possiveis_classificacoes: HashSet<String> =
                        base_dados.iter().map(|dado| dado.1.clone()).collect();

                    let mut lista_n_classificacoes: Vec<(usize, String)> = possiveis_classificacoes
                        .iter()
                        .map(|classificacao| {
                            (
                                base_dados
                                    .iter()
                                    .filter(|dado| &dado.1 == classificacao)
                                    .count(),
                                classificacao.clone(),
                            )
                        })
                        .collect();

                    lista_n_classificacoes.sort_by(|a, b| a.0.partial_cmp(&b.0).unwrap());

                    no = No::Folha(
                        lista_n_classificacoes[lista_n_classificacoes.len() - 1]
                            .1
                            .clone(),
                    );
                } else {
                    no = No::criar_folha(
                        base_dados_so_com_esse_valor_desse_atributo,
                        atributos_ignorados.clone(),
                        possiveis_valores_dos_atributos.clone(),
                    );
                }
                (valor.clone(), no)
            })
            .collect();

        No::Galho(atributo_escolhido, ramos_do_galho)
    }

    pub fn coisa(&self, x: Vec<String>) -> String {
        match self {
            No::Folha(class) => class.clone(),
            No::Galho(atributo, ramos) => {
                let valor_observado_do_atributo = x[atributo.clone()].clone();
                for idx in 0..ramos.len() {
                    if ramos[idx].0 == valor_observado_do_atributo {
                        return ramos[idx].1.coisa(x);
                    }
                }

                println!("tentou dar predict em um vetor com um dos valores desconhecido: {} no atributo {}", valor_observado_do_atributo, atributo);
                panic!();
            }
        }
    }
}

type ArvoreDecisao = No;

pub fn carregar_dados(arq: String) -> Vec<(Vec<String>, String)> {
    let file = File::open(arq).expect("cade o arquivo?");
    let buf = BufReader::new(file);
    let linhas: Vec<String> = buf
        .lines()
        .map(|l| l.expect("Could not parse line"))
        .collect();

    linhas
        .iter()
        .map(|linha| {
            let mut vec: Vec<String> = linha.split(",").map(|e| e.into()).collect();
            let y = vec.remove(vec.len() - 1);
            let x = vec;
            (x, y)
        })
        .collect()
}

fn main() {
    let mut base_dados = carregar_dados("car.data".into());

    //let aa = ArvoreDecisao::novo(base_dados); return;
    let mut rng = thread_rng();
    base_dados.shuffle(&mut rng);

    //deixa a base com 1720 pra fazer o 10-fold igualzinho
    for _ in 0..8 {
        base_dados.pop();
    }

    let mut acertos: Vec<f64> = Vec::new();
    for fold_idx in 0..10 {
        let inicio_teste = 172 * fold_idx;

        let mut testes = Vec::new();
        let mut treino = base_dados.clone();

        for _ in 0..172 {
            testes.push(treino.remove(inicio_teste));
        }

        let arvore = ArvoreDecisao::novo(treino.clone());
        let num_acertos: usize = testes
            .iter()
            .map(|teste| {
                let classificacao_verdadeira = teste.1.clone();
                let predicao = arvore.coisa(teste.0.clone());
                if classificacao_verdadeira == predicao {
                    return 1;
                }

                return 0;
            })
            .sum();

        println!(
            "Acertou {} de 172, {:.3}%",
            num_acertos,
            100.0 * num_acertos as f64 / 172 as f64
        );

        acertos.push(num_acertos as f64);
    }

    let media_num_acertos: f64 = acertos.iter().sum::<f64>() as f64 / acertos.len() as f64;
    println!(
        "Media de acertos de {}/172, {:.3}%",
        media_num_acertos,
        100.0 * media_num_acertos / 172.0
    );
}
