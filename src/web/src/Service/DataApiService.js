import axios from "axios";
import Config from '../Config';


const baseURL = Config.DATA_API_URL;

const getChartDataApi = async (dataTitle) => {
    return axios.get(baseURL + "data/" + dataTitle).then((response) => {
        let result = JSON.parse(response.data.Item.data_content.replace(/'/g, '"'));
        return result;
    }).catch(error => {
        console.log(error);
        throw Error(error);
    });
};

const getCommentsApi = async (sectionId) => {
    return axios.get(baseURL + "comment/" + sectionId).then((response) => {
        let result = response.data.Items;
        return result;
    }).catch(error => {
        console.log(error);
        throw Error(error);
    });
};

const postCommentApi = async (comment) => {

    const postUrl = baseURL + "comment";

    try {
        const response = await axios.post(postUrl, comment);

        const result = {
            status: response.status + "-" + response.statusText,
            headers: response.headers,
            data: response.data,
        };

        return result;
    } catch (error) {
        console.log(error);
        throw Error(error);
    }
};


const DataService = {
    getChartDataApi,
    getCommentsApi,
    postCommentApi
}
export default DataService;