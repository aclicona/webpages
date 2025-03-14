type PasswordErrorCode =
  | 'password_too_short'
  | 'password_too_common'
  | 'password_entirely_numeric'
  | 'password_too_similar'
  | 'password_no_letter'
  | 'password_no_number'
  | 'password_no_special'
  | 'passwords_do_not_match';

// Error code types for email validation
type EmailErrorCode =
  | 'email_invalid'
  | 'email_already_exists'
  | 'email_not_found'
  | 'email_required';

// Error code types for name validation
type NameErrorCode =
  | 'name_required'
  | 'name_too_short'
  | 'name_invalid_characters';
// Error code types for name validation
type ActivationErrorCode =
  | 'invalid_token'
  | 'already_verified'

// Single error object structure
export interface ValidationError {
  code: PasswordErrorCode | EmailErrorCode | NameErrorCode ;
  message?: string;
}

// Single error object structure
export interface ActivationError {
  code: ActivationErrorCode;
  message?: string;
}

// Field-specific error arrays
interface FieldErrors {
  password1?: ValidationError[];
  password2?: ValidationError[];
  email?: ValidationError[];
  name?: ValidationError[];
}
// Field-specific error arrays
export interface ActivationErrors {
  nonFieldErrors?: ActivationError[];
}

// Complete registration errors interface
export interface RegistrationErrors {
  // Field-specific errors
  fieldErrors?: FieldErrors;

  // General errors that aren't field-specific
  generalErrors?: string[];

  // Server or network related errors
  serverError?: {
    code: string;
    message: string;
  };

  // HTTP status code if applicable
  status?: number;

  // Flag to indicate if the error is from the client-side validation
  isClientValidation?: boolean;
}

// Helper type for registration error responses
export interface RegistrationErrorResponse {
  success: false;
  errors: RegistrationErrors;
}

// Helper type for successful registration
export interface RegistrationSuccessResponse {
  success: true;
  data: {
    userId: string;
    email: string;
    requiresEmailVerification: boolean;
  };
}

// Combined type for registration response
type RegistrationResponse = RegistrationErrorResponse | RegistrationSuccessResponse;

// Error message mapping
const ERROR_MESSAGES: Record<PasswordErrorCode | EmailErrorCode | NameErrorCode | ActivationErrorCode, string> = {
  password_too_short: 'La contraseña debe tener al menos 8 caracteres',
  password_too_common: 'La contraseña es demasiado común',
  password_entirely_numeric: 'La contraseña debe contener letras y números',
  password_too_similar: 'La contraseña es muy similar a tu información personal',
  password_no_letter: 'La contraseña debe contener al menos una letra',
  password_no_number: 'La contraseña debe contener al menos un número',
  password_no_special: 'La contraseña debe contener al menos un carácter especial',
  passwords_do_not_match: 'Las contraseñas no coinciden',
  email_invalid: 'El correo electrónico no es válido',
  email_already_exists: 'Este correo electrónico ya está registrado',
  email_not_found: 'Correo electrónico no encontrado',
  email_required: 'El correo electrónico es requerido',
  name_required: 'El nombre es requerido',
  name_too_short: 'El nombre es demasiado corto',
  name_invalid_characters: 'El nombre contiene caracteres no válidos',
  invalid_token: 'El token suministrado no es válido o ha caducado',
  already_verified: 'La cuenta ya se encuentra verificada',
};
export { ERROR_MESSAGES };