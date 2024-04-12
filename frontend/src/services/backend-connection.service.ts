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
    // let formData:FormData = new FormData();
    // formData.append('uploadFile', file, file.name)
    //
    // let headers = new HttpHeaders({
    //   'Content-Type': 'application/octet-stream',
    //   'Accept': 'application/json'
    // });
    //
    // let options = { headers: headers };

    let formParams = new FormData();
    formParams.append('bpmnFile', file)

    // return this.httpClient.post(this.HTTP_BASE_URL + '', formData, options)
    return this.httpClient.post(this.HTTP_BASE_URL + '', formParams)
  }

  testRoute(){
    return this.httpClient.get(
      this.HTTP_BASE_URL + 'test_route'
    );
  }
}
