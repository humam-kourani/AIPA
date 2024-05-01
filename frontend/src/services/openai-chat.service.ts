import {Injectable} from '@angular/core';
import {Subject} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class OpenaiChatService {

  resetSubject = new Subject<any>();
  textualRepresentation = ''
  modelXmlString = ''
  modelSvg = ''

  constructor() {
  }

}
