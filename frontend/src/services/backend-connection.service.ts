import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {environment} from "../environments/environment";


@Injectable({
  providedIn: 'root'
})
export class BackendConnectionService {

  private HTTP_BASE_URL = environment.WEBSERVER_URL

  constructor(private httpClient: HttpClient) { }

  updateConfig(modelName: string | undefined, apiKey: string | undefined){
    return this.httpClient.post(
      this.HTTP_BASE_URL + 'update-config',
      { model_name: modelName, api_key: apiKey }
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
      { parameters: postDataContent }
    );
  }

  testRoute(){
    return this.httpClient.get(
      this.HTTP_BASE_URL + 'test_route'
    );
  }
}
