import { Component } from '@angular/core';
// @ts-ignore
import * as $ from 'jquery';
import {OpenaiChatService} from "../services/openai-chat.service";
import {NbChatModule, NbLayoutModule} from "@nebular/theme";
import {NgForOf, NgIf} from "@angular/common";
import {MatButton} from "@angular/material/button";
import {MatIcon} from "@angular/material/icon";
import {MatProgressBar} from "@angular/material/progress-bar";

// @ts-ignore
@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [
    NbChatModule,
    NbLayoutModule,
    NgForOf,
    MatButton,
    MatIcon,
    MatProgressBar,
    NgIf
  ],
  templateUrl: './chat.component.html',
  styleUrl: './chat.component.scss'
})
export class ChatComponent {

  messages: any[];
  showLoader: boolean = false

  constructor(private openaiChatService: OpenaiChatService) {
    this.messages = this.openaiChatService.loadMessages();
  }


  sendMessage(event: any) {
    this.showLoader = true

    this.messages.push({
      text: event.message,
      date: new Date(),
      reply: true,
      user: {
        name: 'You',
        avatar: './assets/human.png',
      },
    });

    const botReply = this.openaiChatService.reply(event.message);

    if (botReply) {
      setTimeout(() => {
        this.messages.push(botReply);
        this.showLoader = false
      }, 1000);
    }
  }

  resetConversation(){
    this.messages=[]
  }

}
