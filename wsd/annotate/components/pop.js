import {
    LitElement,
    html,
    css
} from 'https://cdn.jsdelivr.net/gh/lit/dist@3/all/lit-all.min.js';

class LinPopComponent extends LitElement {
    static properties = {
        text: { type: String },
        popEvent: { type: String }
    };
    static styles = css`
        .pop:hover {
            background-color:rgb(181, 181, 181);
            cursor: pointer;
        }
    `;

    render() {
        return html`
        <span class="pop" @click="${this._pop}">
          ${this.text}
        </span>
      `;
    }

    _pop() {
        this.dispatchEvent(
            new MesopEvent(this.popEvent, {
                text: this.text,
            }),
        );
    }
}

customElements.define('linpop-component', LinPopComponent);