import React from 'react';
import './TagEditorComponent.css';
import { ContentState, Editor, EditorState, RichUtils, convertFromHTML } from 'draft-js';

class TagEditorComponent extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      editorState: EditorState.createEmpty()
    };
    this.onChange = (editorState) => this.setState({ editorState });
    this.setEditor = (editor) => {
      this.editor = editor;
    };
    this.focusEditor = () => {
      if (this.editor) {
        this.editor.focus();
      }
    };

    this.onBoldClick = this.onBoldClick.bind(this);
    this.onSubmitClick = this.onSubmitClick.bind(this);
  }

  handleKeyCommand = (command) => {
    const newState = RichUtils.handleKeyCommand(this.state.editorState, command)
    if (newState) {
      this.onChange(newState);
    }
    return 'handled';
  }

  handleBeforeInput(chars, editorState, eventTimeStamp) {
    return true;
  }

  handlePastedText(text, html, editorState) {
    return true;
  }

  componentDidMount() {
    this.focusEditor();
  }

  componentDidUpdate(prevProps) {
    if (prevProps === this.props) {
      return;
    }

    const blocksFromHTML = convertFromHTML(this.props.resource);
    const contentState = ContentState.createFromBlockArray(
      blocksFromHTML.contentBlocks,
      blocksFromHTML.entityMap,
    );

    const editorState = EditorState.createWithContent(contentState);
    this.setState({ editorState });
  }

  /** Emulating pressing Ctrl+B */
  onBoldClick() {
    this.onChange(RichUtils.toggleInlineStyle(this.state.editorState, 'BOLD'))
  }

  /** Submits the HTML */
  onSubmitClick() {
    this.props.onSubmit(this.state.editorState.getCurrentContent());
  }

  render() {
    return (
      <div className="editorContainer">
        <div className="editorHeader">
          <div className="btn" onClick={this.onBoldClick}>
            mark as complex
              </div>
          <p>try using the Ctrl+B hotkey</p>
        </div>
        <div className="editors">
          <Editor
            ref={this.setEditor}
            customStyleMap={styleMap}
            editorState={this.state.editorState}
            handleKeyCommand={this.handleKeyCommand}
            handleBeforeInput={this.handleBeforeInput}
            handlePastedText={this.handlePastedText}
            stripPastedStyles={true}
            onChange={this.onChange}
          />
        </div>
        <div className="editorFooter">
          <div className="btn" onClick={this.onSubmitClick} disabled={!this.props.personalInfoIsValid}>
            submit
              </div>
          <div className="btn" onClick={this.props.onSkip}>
            skip
              </div>
        </div>
      </div>
    );
  }
}

const styleMap = {
  'BOLD': {
    'borderRadius': '2pt',
    'backgroundColor': '#faed27',
    'fontWeight': 'bold',
    'paddingLeft': '2pt',
    'paddingRight': '2pt',
    'marginLeft': '1pt',
    'marginRight': '1pt'
  }
};

export default TagEditorComponent;
