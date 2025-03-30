import axios from 'axios';

const BASE_URL = 'http://127.0.0.1:5000/busca';

export const buscarOperadoras = async (termo, page = 1, perPage = 10) => {
    try {
        if (!termo) {
            throw new Error('O termo de busca é obrigatório.');
        }

        const params = new URLSearchParams();
        params.append('termo', termo);
        params.append('page', page);
        params.append('per_page', perPage);

        const url = `${BASE_URL}?${params.toString()}`;
        const response = await axios.get(url);
        return response.data; // Retorna o objeto com total e resultados
    } catch (error) {
        console.error('Erro na requisição:', error);
        // Lança o erro para que o componente possa tratá-lo adequadamente
        throw error;
    }
};
