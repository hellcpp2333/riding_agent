# custom-confirm-dialog Specification

## Purpose
TBD - created by archiving change custom-delete-confirm-dialog. Update Purpose after archive.
## Requirements
### Requirement: Custom confirm dialog for destructive actions
The system SHALL provide a custom confirm dialog component styled consistently with the application's modal design system, for use in destructive actions such as route deletion.

#### Scenario: User confirms deletion
- **WHEN** the confirm dialog is shown and the user clicks the confirm button
- **THEN** the dialog SHALL close and the returned Promise SHALL resolve

#### Scenario: User cancels deletion
- **WHEN** the confirm dialog is shown and the user clicks the cancel button
- **THEN** the dialog SHALL close and the returned Promise SHALL reject with `'cancel'`

#### Scenario: Dialog matches design system
- **WHEN** the confirm dialog is displayed
- **THEN** it SHALL use the same `.modal` overlay and `.modal-content` card styles as route-modal and search-modal
- **AND** the confirm button SHALL use a danger color style consistent with `.btn-danger`

