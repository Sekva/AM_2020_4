#[derive(Debug)]
pub struct Neuronio {
    w: Vec<f64>,
    erro: f64,
}

impl Neuronio {
    pub fn novo() -> Neuronio {
        Neuronio {
            w: Vec::new(),
            erro: 0.0,
        }
    }

    pub fn novo_com_pesos(w: &Vec<f64>) -> Neuronio {
        Neuronio {
            w: w.clone(),
            erro: 0.0,
        }
    }

    pub fn aplicar_entrada(w: &Vec<f64>, entrada: &Vec<f64>) -> f64 {
        let tamanho = entrada.len().min(w.len());

        let mut v: f64 = 0.0;
        for i in 0..tamanho {
            v += w[i] * entrada[i];
        }

        if v > 0.0 {
            1.0
        } else {
            0.0
        }
    }

    pub fn treinar(
        &self,
        dados: &Vec<(Vec<f64>, u8)>,
        eta: f64,
        erro_max: f64,
        epocas_total: i32,
    ) -> Neuronio {
        let debug = false;

        let mut pesos: Vec<f64> = Vec::new();
        for _ in 0..dados[0].0.len() {
            pesos.push(0.0);
        }

        let mut epoca_atual = 0;
        // se vc considera erro 0, erro total tem que ser maior que o maximo pra garantir o primeiro passo
        let mut erro_total = erro_max + 1.0;

        let mut loop_epoca = false;

        if epocas_total > 0 {
            loop_epoca = true;
        }

        loop {
            if loop_epoca {
                if epoca_atual >= epocas_total {
                    break;
                }
            } else {
                if erro_total <= erro_max {
                    break;
                }
            }

            if debug {
                std::thread::sleep(std::time::Duration::from_secs(1));
            }
            epoca_atual += 1;
            let mut atualizacoes = 0;

            for dado in dados.clone() {
                let x = dado.0.clone();
                let y = dado.1;
                let d = x.len();

                let f = Neuronio::aplicar_entrada(&pesos, &x);
                let dt: f64 = y as f64 - f;
                let erro = dt * dt;

                if erro > 0.0 {
                    atualizacoes += 1;

                    for j in 0..d {
                        pesos[j] += eta * x[j] * dt;
                    }
                }
            }

            //println!(
            //    "Na epoca {} foram {} atualizações",
            //    epoca_atual, atualizacoes
            //);
            //println!("Pesos: {:?}", pesos);
            if debug {
                continue;
            }
            erro_total = 0.0;

            for dado in dados.clone() {
                let x = dado.0.clone();
                let y = dado.1;

                let f = Neuronio::aplicar_entrada(&pesos, &x);
                let dt: f64 = y as f64 - f;

                erro_total += dt * dt;
            }

            //println!("Erro total: {}", erro_total);
            //println!();
        }

        Neuronio {
            w: pesos,
            erro: erro_total,
        }
    }
    pub fn erro(&self, dados: &Vec<(Vec<f64>, u8)>) -> f64 {
        let mut erro_total = 0.0;

        for dado in dados.clone() {
            let x = dado.0.clone();
            let y = dado.1;

            let f = Neuronio::aplicar_entrada(&self.w, &x);
            let dt: f64 = y as f64 - f;

            erro_total += dt * dt;
        }

        erro_total
    }
}
