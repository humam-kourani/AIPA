import {Injectable} from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class OpenaiChatService {

  constructor() {
  }

  loadMessages() {
    return [{
      text: 'Hi Wassup??',
      date: new Date(),
      reply: true,
      user: {
        name: 'You',
        avatar: './assets/human.png',
      },
    },{
      text: 'Hello there',
      date: new Date(),
      reply: false,
      user: {
        name: 'Bot',
        avatar: './assets/robot.png',
      }
    }
    ]
  }

  reply(message: any){
    return {
      text: 'Vestibulum nec vehicula sapien. In et vulputate ligula. Fusce tristique, nibh id condimentum dapibus, purus dolor congue neque, viverra laoreet ex risus id elit. Nunc quis ornare dui. Mauris convallis, dui vel porttitor laoreet, ex est convallis arcu, id tristique ligula orci non ex. Nunc malesuada diam ut sem suscipit tincidunt. Donec sed purus posuere, pellentesque ante id, faucibus arcu. Vivamus malesuada metus non ex varius volutpat. Vestibulum rhoncus sem nulla, eget suscipit diam eleifend nec. Etiam malesuada elit eu odio maximus, eu molestie neque suscipit. Nam eget luctus nisi. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin imperdiet tortor quis ipsum lobortis suscipit. Aliquam ut vulputate massa, vel molestie urna.',
      date: new Date(),
      reply: false,
      user: {
        name: 'Bot',
        avatar: './assets/robot.png',
      }
    }
  }
}
