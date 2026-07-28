export interface FormField {
  key: string;
  label: string;
  type:
    | "text"
    | "textarea"
    | "select"
    | "multiSelect"
    | "switch"
    | "number"
    | "file"
    | "mediaPicker";
  required?: boolean;
  rows?: number;
  optionsGetter?: () => Promise<{ label: string; value: any }[]>;
  placeholder?: string;
  uploadApi?: (file: File) => Promise<any>;
  accept?: string;
}

export interface FormConfig<TData> {
  fields: FormField[];
  saveApi: (data: TData, id?: string) => Promise<any>;
}
