import { LitElement, html, css } from 'lit';


class LinDocElement extends LitElement {
    static properties = {
        tokens: { type: Array },
        cur: { type: Number },
        popEvent: { type: String }
    }
    static styles = css`
        .tok {
            padding: 2px
        }
        .selected {
            background-color:rgb(181, 181, 181);
            border-radius: 4px;
        }
    `;

    render() {
        return html`
        <div class="doc">
            ${this.tokens.map((token, i) => html`
                <span class="${i === this.cur ? 'selected' : ''} tok" @click="${() => this._pop(token)}" class="tok">
                    ${token.text}
                </span>`
        )}
        </div>
      `;
    }

    _pop(token) {
        this.dispatchEvent(
            new MesopEvent(this.popEvent, {
                text: token.text,
            })
        );
    }
}


class LinEntryElement extends LitElement {
    static properties = {
        entry: { type: Object },
        selected: { type: Boolean },
        chosenEvent: { type: String }
    }
    static styles = css`
        .entry {
            min-width: 300px;
            max-width: 300px;
            border-radius: 8px;
            padding: 16px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.12);
        }
        .selected {
            box-shadow: 0 4px 8px rgb(124, 149, 249);
            background-color:  rgb(124, 149, 249);
        }
        .entry:hover {
            box-shadow: 0 4px 8px rgb(192, 203, 249);
            cursor: pointer;
            background-color: lightgrey;
            &.selected {
                background-color:  rgb(124, 149, 249);
            }
        }
        .kanjis {
            display: flex;
            font-weight: bold;
        }
        .readings {
            display: flex;
            color: steelblue;
        }
        .sense {
            display: flex;
            flex-wrap: wrap;
        }
    `;

    render() {
        return html`
        <div class="entry ${this.selected ? 'selected' : ''}" @click="${this._onChosen}">
            <div class="kanjis">
                ${this.entry.k_ele.map((kanji) => html`
                    <div class="kanji text-3xl font-bold underline">
                        ${kanji.keb}, &nbsp;
                    </div>
                `)}
            </div>
            <div class="readings">
                ${this.entry.r_ele.map((reading) => html`
                    <div class="reading">
                        ${reading.reb}, &nbsp;
                    </div>
                `)}
            </div>
            <div class="senses">
                ${this.entry.sense.map((sense, i) => html`
                    <div class="sense">
                        ${i}. ${sense.gloss.map(g => g.text).join(", ")}
                    </div>
                `)}
            </div>
        </div>
      `;
    }

    _onChosen() {
        const ent = this.renderRoot?.querySelector('.entry')
        ent.style.background = 'light-blue';
        this.dispatchEvent(
            new MesopEvent(this.chosenEvent, {
                text: this.entry.ent_seq,
            })
        );
    }
}


customElements.define('lin-entry', LinEntryElement);
customElements.define('lin-doc', LinDocElement);
