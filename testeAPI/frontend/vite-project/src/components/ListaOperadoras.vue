<template>
    <div class="min-h-screen flex items-center justify-center bg-blue-100">
        <div class="max-w-2xl mx-auto mt-10 p-6 bg-white shadow-lg rounded-xl">
            <h2 class="text-2xl font-semibold text-gray-700 mb-4 text-center">
                Buscar Operadoras
            </h2>

            <div class="flex gap-2 mb-4">
                <input
                    type="text"
                    v-model="termoBusca"
                    placeholder="Digite a razão social"
                    class="w-11/12 p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <button
                    @click="buscar"
                    class="px-4 py-2 rounded-md font-semibold text-white bg-blue-500 hover:bg-blue-600 transition-all duration-300 shadow-md hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 border border-blue-700"
                >
                    Buscar
                </button>
            </div>

            <p v-if="erroBusca" class="text-red-600 bg-red-50 p-2 rounded-md">
                {{ erroBusca }}
            </p>

            <p
                v-if="buscaRealizada && totalResultados === 0 && !erroBusca"
                class="text-red-600 bg-red-50 p-2 rounded-md"
            >
                Nenhum resultado encontrado para sua busca "{{
                    termoBuscaBusca
                }}"
            </p>

            <p
                v-else-if="buscaRealizada && totalResultados > 0 && !erroBusca"
                class="text-lg font-semibold text-blue-600"
            >
                Total de {{ totalResultados }} resultados encontrados
            </p>

            <ol
                v-if="
                    buscaRealizada &&
                    operadoras &&
                    operadoras.length > 0 &&
                    !erroBusca
                "
                class="space-y-3 list-inside"
            >
                <li
                    v-for="(operadora, index) in operadoras"
                    :key="operadora.Registro_ANS"
                    class="p-4 bg-gray-100 rounded-lg shadow hover:bg-gray-200 transition-colors duration-200"
                >
                    <span class="font-semibold">
                        {{ (paginaAtual - 1) * itensPorPagina + index + 1 }}.
                        {{ operadora.Razao_Social }}
                    </span>
                </li>
            </ol>

            <div
                v-if="buscaRealizada && totalResultados > 0 && !erroBusca"
                class="flex justify-center mt-4"
            >
                <button
                    :disabled="paginaAtual === 1"
                    @click="paginaAnterior"
                    class="px-4 py-2 mx-1 rounded-md bg-gray-200 hover:bg-gray-300"
                >
                    Anterior
                </button>
                <span class="px-4 py-2 mx-1 rounded-md bg-gray-200"
                    >Página {{ paginaAtual }}</span
                >
                <button
                    :disabled="operadoras && operadoras.length < itensPorPagina"
                    @click="proximaPagina"
                    class="px-4 py-2 mx-1 rounded-md bg-gray-200 hover:bg-gray-300"
                >
                    Próxima
                </button>
            </div>
        </div>
    </div>
</template>

<script>
import { ref } from 'vue';
import { buscarOperadoras } from '../service/OperadorasService.js';

export default {
    setup() {
        const termoBusca = ref('');
        const operadoras = ref([]);
        const buscaRealizada = ref(false);
        const termoBuscaBusca = ref('');
        const paginaAtual = ref(1);
        const itensPorPagina = ref(10);
        const totalResultados = ref(0);
        const erroBusca = ref('');

        const buscar = async () => {
            erroBusca.value = ''; // Limpa qualquer erro anterior
            if (!termoBusca.value.trim()) {
                erroBusca.value = 'Por favor, digite um termo de busca.';
                return;
            }

            termoBuscaBusca.value = termoBusca.value;
            try {
                const data = await buscarOperadoras(
                    termoBusca.value,
                    paginaAtual.value,
                    itensPorPagina.value
                );
                if (data) {
                    console.log('Dados recebidos da API:', data);
                    operadoras.value = data.resultados;
                    console.log('Operadoras:', operadoras.value);
                    totalResultados.value = data.total;
                    console.log('Total de resultados:', totalResultados.value);
                }
            } catch (error) {
                console.error('Erro ao buscar operadoras:', error);
                erroBusca.value = 'Ocorreu um erro ao buscar os dados.';
                operadoras.value = [];
                totalResultados.value = 0;
            }
            buscaRealizada.value = true;
        };

        const proximaPagina = () => {
            paginaAtual.value++;
            buscar();
        };

        const paginaAnterior = () => {
            if (paginaAtual.value > 1) {
                paginaAtual.value--;
                buscar();
            }
        };

        return {
            termoBusca,
            operadoras,
            buscar,
            buscaRealizada,
            termoBuscaBusca,
            paginaAtual,
            itensPorPagina,
            totalResultados,
            proximaPagina,
            paginaAnterior,
            erroBusca,
        };
    },
};
</script>
