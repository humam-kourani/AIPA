import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {environment} from "../environments/environment";


@Injectable({
  providedIn: 'root'
})
export class BackendConnectionService {

  private HTTP_BASE_URL: string;

  constructor(private httpClient: HttpClient) {
    if (window.location.hostname === 'aipa.fit.fraunhofer.de') {
      this.HTTP_BASE_URL = environment.WEBSERVER_URL_REMOTE;
    } else {
      this.HTTP_BASE_URL = environment.WEBSERVER_URL_LOCAL;
    }
  }

  updateConfig(modelName: string | undefined, apiKey: string | undefined, apiURL: string | undefined, azureEndpoint: string | undefined){
    return this.httpClient.post(
      this.HTTP_BASE_URL + 'update-config',
      { model_name: modelName, api_key: apiKey, api_url: apiURL, azure_endpoint: azureEndpoint }
    );
  }

  uploadBPMN(file: File){
    let formParams = new FormData();
    formParams.append('bpmnFile', file)

    // return this.httpClient.post(this.HTTP_BASE_URL + '', formData, options)
    return this.httpClient.post(this.HTTP_BASE_URL + '', formParams)
  }

  resetConversation(){
    return this.httpClient.post(
      this.HTTP_BASE_URL + 'reset_conversation',
      { }
    );
  }

  sendMessage(postDataContent: any){
    return this.httpClient.post(
      this.HTTP_BASE_URL + 'chat_with_llm',
      postDataContent
    );
  }

  testRoute(){
    return this.httpClient.get(
      this.HTTP_BASE_URL + 'test_route'
    );
  }
}
