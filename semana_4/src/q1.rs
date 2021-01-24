use crate::neuronio::Neuronio;
use rand::distributions::{Distribution, Uniform};
use std::fs::File;
use std::vec::Vec;

pub fn pegar_base_iris() -> Vec<(Vec<f64>, u8)> {
    let file = File::open("iris.data").unwrap();
    let mut rdr = csv::ReaderBuilder::new()
        .has_headers(false)
        .from_reader(file);

    let mut arr: Vec<(Vec<f64>, u8)> = Vec::new();
    for result in rdr.records() {
        let record = result.unwrap();

        let mut x: Vec<f64> = Vec::new();

        for i in 0..4 {
            x.push(record.get(i).unwrap().parse().unwrap());
        }

        arr.push((x, record.get(4).unwrap().parse().unwrap()));
    }

    arr
}

pub fn iris_treino_teste() -> (Vec<(Vec<f64>, u8)>, Vec<(Vec<f64>, u8)>) {
    let mut base_treino: Vec<(Vec<f64>, u8)> = Vec::new();
    let mut base_teste: Vec<(Vec<f64>, u8)> = Vec::new();

    let arr = pegar_base_iris();

    for d in arr.clone() {
        for classe in 0..3 {
            if d.clone().1 == classe {
                //setosa
                if base_treino.iter().filter(|i| i.1 == classe).count() < 25 {
                    //conta quantas setosas tem no treino
                    base_treino.push(d.clone());
                } else {
                    base_teste.push(d.clone());
                }
            }
        }
    }

    (base_treino, base_teste)
}

pub fn setar_classe_alvo(classe_alvo: u8, dados: Vec<(Vec<f64>, u8)>) -> Vec<(Vec<f64>, u8)> {
    dados
        .iter()
        .map(|i| {
            if i.1 == classe_alvo {
                return (i.0.clone(), 1);
            } else {
                return (i.0.clone(), 0);
            }
        })
        .collect()
}

fn q_1_a_b(classe_alvo: u8, epocas: i32) {
    let (mut base_treino, mut base_teste) = iris_treino_teste();

    base_treino = setar_classe_alvo(classe_alvo, base_treino);
    base_teste = setar_classe_alvo(classe_alvo, base_teste);

    let neuronio_treinado = Neuronio::novo().treinar(&base_treino, 0.000001, 0.0, epocas);
    //println!("{:?}\n", neuronio_treinado);

    let erro = neuronio_treinado.erro(&base_teste);

    println!(
        "Erro na base de teste: {}%, {}/{}",
        100.0 * erro / base_teste.len() as f64,
        erro,
        base_teste.len()
    );
}

pub fn q_1_c() {
    let mut pesos_iniciais = vec![0.38, 0.56, 0.67, 0.32, 0.13];
    let etas: Vec<f64> = vec![0.1, 1.0, 10.0];

    let testes = vec![("setosa", 0, 0), ("virginica", 2, 100)];

    for teste in testes {
        let mut taxas_acertos: Vec<(f64, f64, f64)> = Vec::new();
        let (mut base_treino, mut base_teste) = iris_treino_teste();
        base_treino = setar_classe_alvo(teste.1, base_treino);
        base_teste = setar_classe_alvo(teste.1, base_teste);
        for _ in 0..30 {
            pesos_iniciais = pesos_iniciais
                .iter()
                .map(|_| {
                    let between = Uniform::from(0..10001);
                    let mut rng = rand::thread_rng();
                    (between.sample(&mut rng) as f64) / 10001 as f64
                })
                .collect();

            let resultados: Vec<f64> = etas
                .iter()
                .map(|eta| {
                    let neuronio_treinado = Neuronio::novo_com_pesos(&pesos_iniciais).treinar(
                        &base_treino,
                        *eta,
                        0.0,
                        teste.2,
                    );
                    //println!(
                    //   "inicial: {:?}, eta:{} peso:{:?}\n",
                    //   pesos_iniciais, eta, neuronio_treinado
                    //);
                    let erro = neuronio_treinado.erro(&base_teste);
                    erro / base_teste.len() as f64
                })
                .collect();
            taxas_acertos.push((resultados[0], resultados[1], resultados[2]));
        }

        println!("Resultados {}", teste.0);

        let mut medias = taxas_acertos
            .iter()
            .fold((0f64, 0f64, 0f64), |mut soma, &el| {
                soma.0 += el.0;
                soma.1 += el.1;
                soma.2 += el.2;
                soma
            });

        medias.0 = medias.0 / taxas_acertos.len() as f64;
        medias.1 = medias.1 / taxas_acertos.len() as f64;
        medias.2 = medias.2 / taxas_acertos.len() as f64;

        println!("Media η = 0.1: {:?}", medias.0);
        println!("Media η = 1: {:?}", medias.1);
        println!("Media η = 10: {:?}", medias.2);

        let diff_quadradas: Vec<(f64, f64, f64)> = taxas_acertos
            .iter()
            .map(|taxa_acerto| {
                let mut tr = (0f64, 0f64, 0f64);
                tr.0 = (taxa_acerto.0 - medias.0) * (taxa_acerto.0 - medias.0);
                tr.1 = (taxa_acerto.1 - medias.1) * (taxa_acerto.1 - medias.1);
                tr.2 = (taxa_acerto.2 - medias.2) * (taxa_acerto.2 - medias.2);

                tr
            })
            .collect();

        let soma_diff_quadradas =
            diff_quadradas
                .iter()
                .fold((0f64, 0f64, 0f64), |mut soma, &el| {
                    soma.0 += el.0;
                    soma.1 += el.1;
                    soma.2 += el.2;
                    soma
                });

        let desvios_padroes = (
            (soma_diff_quadradas.0 / diff_quadradas.len() as f64).sqrt(),
            (soma_diff_quadradas.1 / diff_quadradas.len() as f64).sqrt(),
            (soma_diff_quadradas.2 / diff_quadradas.len() as f64).sqrt(),
        );

        println!("DP η = 0.1: {:?}", desvios_padroes.0);
        println!("DP η = 1: {:?}", desvios_padroes.1);
        println!("DP η = 10: {:?}", desvios_padroes.2);
    }
}

pub fn main_q1() {
    //q_1_a_b(0, 0);
    //q_1_a_b(2, 0);
    //q_1_a_b(2, 100);
    q_1_c();
}
