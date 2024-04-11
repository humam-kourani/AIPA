import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class BackendConnectionService {

  private HTTP_BASE_URL = 'http://127.0.0.1:5000/'

  constructor(private httpClient: HttpClient) { }

  updateConfig(modelName: string | undefined, apiKey: string | undefined){
    return this.httpClient.post(
      this.HTTP_BASE_URL + 'update-config',
      { model_name: modelName, api_key: apiKey }
    );
  }

  testRoute(){
    return this.httpClient.get(
      this.HTTP_BASE_URL + 'test_route'
    );
  }
}
