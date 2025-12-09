import customtkinter as ctk
from tkinter import filedialog, messagebox
import os

class CryptoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Cấu hình cửa sổ chính
        self.title("Lab 06 - Review of Encryption Algorithms")
        self.geometry("1000x700")
        
        # Thiết lập theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Tạo tabview
        self.tabview = ctk.CTkTabview(self, width=950, height=650)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Thêm các tab
        self.tab_caesar = self.tabview.add("Caesar Cipher")
        self.tab_mono = self.tabview.add("Mono-alphabetic")
        self.tab_vigenere = self.tabview.add("Vigenère Cipher")
        self.tab_des = self.tabview.add("DES")
        self.tab_aes = self.tabview.add("AES")
        
        # Khởi tạo giao diện cho từng tab
        self.setup_caesar_tab()
        self.setup_mono_tab()
        self.setup_vigenere_tab()
        self.setup_des_tab()
        self.setup_aes_tab()
    
    def setup_caesar_tab(self):
        """Giao diện cho Caesar Cipher"""
        # Frame chính
        main_frame = ctk.CTkFrame(self.tab_caesar)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tiêu đề
        title = ctk.CTkLabel(main_frame, text="Caesar Cipher - Brute Force Attack", 
                            font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=15)
        
        # Frame chứa các controls với grid
        controls_frame = ctk.CTkFrame(main_frame)
        controls_frame.pack(fill="x", padx=40, pady=10)
        
        # Input file row
        ctk.CTkLabel(controls_frame, text="Ciphertext File:", 
                    font=ctk.CTkFont(size=14), width=140, anchor="w").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.caesar_input_entry = ctk.CTkEntry(controls_frame, width=500)
        self.caesar_input_entry.grid(row=0, column=1, padx=10, pady=10)
        ctk.CTkButton(controls_frame, text="Browse", width=100,
                     command=lambda: self.browse_file(self.caesar_input_entry)).grid(row=0, column=2, padx=10, pady=10)
        
        # Output file row
        ctk.CTkLabel(controls_frame, text="Output File:", 
                    font=ctk.CTkFont(size=14), width=140, anchor="w").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.caesar_output_entry = ctk.CTkEntry(controls_frame, width=500)
        self.caesar_output_entry.grid(row=1, column=1, padx=10, pady=10)
        ctk.CTkButton(controls_frame, text="Browse", width=100,
                     command=lambda: self.save_file(self.caesar_output_entry)).grid(row=1, column=2, padx=10, pady=10)
        
        # Text area cho kết quả
        result_label = ctk.CTkLabel(main_frame, text="Result Preview:", 
                                   font=ctk.CTkFont(size=14))
        result_label.pack(pady=(20, 5))
        
        self.caesar_result_text = ctk.CTkTextbox(main_frame, width=850, height=300)
        self.caesar_result_text.pack(padx=20, pady=5)
        
        # Button thực thi
        btn_frame = ctk.CTkFrame(main_frame)
        btn_frame.pack(pady=20)
        
        ctk.CTkButton(btn_frame, text="🔓 Crack Caesar Cipher", width=200, height=40,
                     font=ctk.CTkFont(size=14, weight="bold"),
                     command=self.crack_caesar).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Clear", width=100, height=40,
                     command=self.clear_caesar).pack(side="left", padx=10)
    
    def setup_mono_tab(self):
        """Giao diện cho Mono-alphabetic Substitution"""
        main_frame = ctk.CTkFrame(self.tab_mono)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        title = ctk.CTkLabel(main_frame, text="Mono-alphabetic Substitution - Frequency Analysis", 
                            font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=15)
        
        # Frame chứa các controls với grid
        controls_frame = ctk.CTkFrame(main_frame)
        controls_frame.pack(fill="x", padx=40, pady=10)
        
        # Input file row
        ctk.CTkLabel(controls_frame, text="Ciphertext File:", 
                    font=ctk.CTkFont(size=14), width=140, anchor="w").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.mono_input_entry = ctk.CTkEntry(controls_frame, width=500)
        self.mono_input_entry.grid(row=0, column=1, padx=10, pady=10)
        ctk.CTkButton(controls_frame, text="Browse", width=100,
                     command=lambda: self.browse_file(self.mono_input_entry)).grid(row=0, column=2, padx=10, pady=10)
        
        # Output file row
        ctk.CTkLabel(controls_frame, text="Output File:", 
                    font=ctk.CTkFont(size=14), width=140, anchor="w").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.mono_output_entry = ctk.CTkEntry(controls_frame, width=500)
        self.mono_output_entry.grid(row=1, column=1, padx=10, pady=10)
        ctk.CTkButton(controls_frame, text="Browse", width=100,
                     command=lambda: self.save_file(self.mono_output_entry)).grid(row=1, column=2, padx=10, pady=10)
        
        # Result preview
        result_label = ctk.CTkLabel(main_frame, text="Result Preview:", 
                                   font=ctk.CTkFont(size=14))
        result_label.pack(pady=(20, 5))
        
        self.mono_result_text = ctk.CTkTextbox(main_frame, width=850, height=300)
        self.mono_result_text.pack(padx=20, pady=5)
        
        # Buttons
        btn_frame = ctk.CTkFrame(main_frame)
        btn_frame.pack(pady=20)
        
        ctk.CTkButton(btn_frame, text="🔍 Analyze & Decrypt", width=200, height=40,
                     font=ctk.CTkFont(size=14, weight="bold"),
                     command=self.crack_mono).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Clear", width=100, height=40,
                     command=self.clear_mono).pack(side="left", padx=10)
    
    def setup_vigenere_tab(self):
        """Giao diện cho Vigenère Cipher"""
        main_frame = ctk.CTkFrame(self.tab_vigenere)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        title = ctk.CTkLabel(main_frame, text="Vigenère Cipher - Kasiski & IC Analysis", 
                            font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=15)
        
        # Frame chứa các controls với grid
        controls_frame = ctk.CTkFrame(main_frame)
        controls_frame.pack(fill="x", padx=40, pady=10)
        
        # Input file row
        ctk.CTkLabel(controls_frame, text="Ciphertext File:", 
                    font=ctk.CTkFont(size=14), width=140, anchor="w").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.vigenere_input_entry = ctk.CTkEntry(controls_frame, width=500)
        self.vigenere_input_entry.grid(row=0, column=1, padx=10, pady=10)
        ctk.CTkButton(controls_frame, text="Browse", width=100,
                     command=lambda: self.browse_file(self.vigenere_input_entry)).grid(row=0, column=2, padx=10, pady=10)
        
        # Output file row
        ctk.CTkLabel(controls_frame, text="Output File:", 
                    font=ctk.CTkFont(size=14), width=140, anchor="w").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.vigenere_output_entry = ctk.CTkEntry(controls_frame, width=500)
        self.vigenere_output_entry.grid(row=1, column=1, padx=10, pady=10)
        ctk.CTkButton(controls_frame, text="Browse", width=100,
                     command=lambda: self.save_file(self.vigenere_output_entry)).grid(row=1, column=2, padx=10, pady=10)
        
        # Result preview
        result_label = ctk.CTkLabel(main_frame, text="Result Preview:", 
                                   font=ctk.CTkFont(size=14))
        result_label.pack(pady=(20, 5))
        
        self.vigenere_result_text = ctk.CTkTextbox(main_frame, width=850, height=300)
        self.vigenere_result_text.pack(padx=20, pady=5)
        
        # Buttons
        btn_frame = ctk.CTkFrame(main_frame)
        btn_frame.pack(pady=20)
        
        ctk.CTkButton(btn_frame, text="🔑 Crack Vigenère", width=200, height=40,
                     font=ctk.CTkFont(size=14, weight="bold"),
                     command=self.crack_vigenere).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Clear", width=100, height=40,
                     command=self.clear_vigenere).pack(side="left", padx=10)
    
    def setup_des_tab(self):
        """Giao diện cho DES"""
        main_frame = ctk.CTkFrame(self.tab_des)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        title = ctk.CTkLabel(main_frame, text="DES Encryption/Decryption", 
                            font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=15)
        
        # Frame chứa các controls với grid
        controls_frame = ctk.CTkFrame(main_frame)
        controls_frame.pack(fill="x", padx=40, pady=10)
        
        # Mode selection row
        ctk.CTkLabel(controls_frame, text="Operation Mode:", 
                    font=ctk.CTkFont(size=14), width=140, anchor="w").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        mode_frame = ctk.CTkFrame(controls_frame)
        mode_frame.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky="w")
        self.des_mode_var = ctk.StringVar(value="ECB")
        ctk.CTkRadioButton(mode_frame, text="ECB", variable=self.des_mode_var, value="ECB").pack(side="left", padx=10)
        ctk.CTkRadioButton(mode_frame, text="CBC", variable=self.des_mode_var, value="CBC").pack(side="left", padx=10)
        ctk.CTkRadioButton(mode_frame, text="CFB", variable=self.des_mode_var, value="CFB").pack(side="left", padx=10)
        ctk.CTkRadioButton(mode_frame, text="OFB", variable=self.des_mode_var, value="OFB").pack(side="left", padx=10)
        
        # Action selection row
        ctk.CTkLabel(controls_frame, text="Action:", 
                    font=ctk.CTkFont(size=14), width=140, anchor="w").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        action_frame = ctk.CTkFrame(controls_frame)
        action_frame.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky="w")
        self.des_action_var = ctk.StringVar(value="encrypt")
        ctk.CTkRadioButton(action_frame, text="Encrypt", variable=self.des_action_var, value="encrypt").pack(side="left", padx=10)
        ctk.CTkRadioButton(action_frame, text="Decrypt", variable=self.des_action_var, value="decrypt").pack(side="left", padx=10)
        
        # Key input row
        ctk.CTkLabel(controls_frame, text="Key (8 bytes/hex):", 
                    font=ctk.CTkFont(size=14), width=140, anchor="w").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.des_key_entry = ctk.CTkEntry(controls_frame, width=350, placeholder_text="Enter 16 hex characters")
        self.des_key_entry.grid(row=2, column=1, padx=10, pady=10)
        ctk.CTkButton(controls_frame, text="Generate Random", width=150,
                     command=self.generate_des_key).grid(row=2, column=2, padx=10, pady=10)
        
        # IV input row
        ctk.CTkLabel(controls_frame, text="IV (8 bytes/hex):", 
                    font=ctk.CTkFont(size=14), width=140, anchor="w").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.des_iv_entry = ctk.CTkEntry(controls_frame, width=350, placeholder_text="Required for CBC/CFB/OFB")
        self.des_iv_entry.grid(row=3, column=1, padx=10, pady=10)
        ctk.CTkButton(controls_frame, text="Generate Random", width=150,
                     command=self.generate_des_iv).grid(row=3, column=2, padx=10, pady=10)
        
        # Input file row
        ctk.CTkLabel(controls_frame, text="Input File:", 
                    font=ctk.CTkFont(size=14), width=140, anchor="w").grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.des_input_entry = ctk.CTkEntry(controls_frame, width=350)
        self.des_input_entry.grid(row=4, column=1, padx=10, pady=10)
        ctk.CTkButton(controls_frame, text="Browse", width=150,
                     command=lambda: self.browse_file(self.des_input_entry)).grid(row=4, column=2, padx=10, pady=10)
        
        # Output file row
        ctk.CTkLabel(controls_frame, text="Output File:", 
                    font=ctk.CTkFont(size=14), width=140, anchor="w").grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.des_output_entry = ctk.CTkEntry(controls_frame, width=350)
        self.des_output_entry.grid(row=5, column=1, padx=10, pady=10)
        ctk.CTkButton(controls_frame, text="Browse", width=150,
                     command=lambda: self.save_file(self.des_output_entry)).grid(row=5, column=2, padx=10, pady=10)
        
        # Result area
        result_label = ctk.CTkLabel(main_frame, text="Result Preview:", 
                                   font=ctk.CTkFont(size=14))
        result_label.pack(pady=(10, 5))
        
        self.des_result_text = ctk.CTkTextbox(main_frame, width=850, height=150)
        self.des_result_text.pack(padx=20, pady=5)
        
        # Buttons
        btn_frame = ctk.CTkFrame(main_frame)
        btn_frame.pack(pady=15)
        
        ctk.CTkButton(btn_frame, text="🔐 Execute DES", width=200, height=40,
                     font=ctk.CTkFont(size=14, weight="bold"),
                     command=self.execute_des).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Clear", width=100, height=40,
                     command=self.clear_des).pack(side="left", padx=10)
    
    def setup_aes_tab(self):
        """Giao diện cho AES"""
        main_frame = ctk.CTkFrame(self.tab_aes)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        title = ctk.CTkLabel(main_frame, text="AES Encryption/Decryption", 
                            font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=15)
        
        # Mode selection
        mode_frame = ctk.CTkFrame(main_frame)
        mode_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(mode_frame, text="Operation Mode:", 
                    font=ctk.CTkFont(size=14)).pack(side="left", padx=10)
        self.aes_mode_var = ctk.StringVar(value="ECB")
        ctk.CTkRadioButton(mode_frame, text="ECB", variable=self.aes_mode_var, 
                          value="ECB").pack(side="left", padx=10)
        ctk.CTkRadioButton(mode_frame, text="CBC", variable=self.aes_mode_var, 
                          value="CBC").pack(side="left", padx=10)
        ctk.CTkRadioButton(mode_frame, text="CFB", variable=self.aes_mode_var, 
                          value="CFB").pack(side="left", padx=10)
        ctk.CTkRadioButton(mode_frame, text="OFB", variable=self.aes_mode_var, 
                          value="OFB").pack(side="left", padx=10)
        
        # Action selection
        action_frame = ctk.CTkFrame(main_frame)
        action_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(action_frame, text="Action:", 
                    font=ctk.CTkFont(size=14)).pack(side="left", padx=10)
        self.aes_action_var = ctk.StringVar(value="encrypt")
        ctk.CTkRadioButton(action_frame, text="Encrypt", variable=self.aes_action_var, 
                          value="encrypt").pack(side="left", padx=10)
        ctk.CTkRadioButton(action_frame, text="Decrypt", variable=self.aes_action_var, 
                          value="decrypt").pack(side="left", padx=10)
        
        # Key size selection
        keysize_frame = ctk.CTkFrame(main_frame)
        keysize_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(keysize_frame, text="Key Size:", 
                    font=ctk.CTkFont(size=14)).pack(side="left", padx=10)
        self.aes_keysize_var = ctk.StringVar(value="128")
        ctk.CTkRadioButton(keysize_frame, text="AES-128 (16 bytes)", 
                          variable=self.aes_keysize_var, value="128").pack(side="left", padx=10)
        ctk.CTkRadioButton(keysize_frame, text="AES-192 (24 bytes)", 
                          variable=self.aes_keysize_var, value="192").pack(side="left", padx=10)
        ctk.CTkRadioButton(keysize_frame, text="AES-256 (32 bytes)", 
                          variable=self.aes_keysize_var, value="256").pack(side="left", padx=10)
        
        # Key input
        key_frame = ctk.CTkFrame(main_frame)
        key_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(key_frame, text="Key (hex):", 
                    font=ctk.CTkFont(size=14)).pack(side="left", padx=10)
        self.aes_key_entry = ctk.CTkEntry(key_frame, width=300, placeholder_text="Enter key in hex")
        self.aes_key_entry.pack(side="left", padx=5)
        ctk.CTkButton(key_frame, text="Generate Random", width=150,
                     command=self.generate_aes_key).pack(side="left", padx=5)
        
        # IV input
        iv_frame = ctk.CTkFrame(main_frame)
        iv_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(iv_frame, text="IV (16 bytes/hex):", 
                    font=ctk.CTkFont(size=14)).pack(side="left", padx=10)
        self.aes_iv_entry = ctk.CTkEntry(iv_frame, width=300, placeholder_text="Required for CBC/CFB/OFB")
        self.aes_iv_entry.pack(side="left", padx=5)
        ctk.CTkButton(iv_frame, text="Generate Random", width=150,
                     command=self.generate_aes_iv).pack(side="left", padx=5)
        
        # Input/Output files
        io_frame = ctk.CTkFrame(main_frame)
        io_frame.pack(fill="x", padx=20, pady=10)
        
        left_col = ctk.CTkFrame(io_frame)
        left_col.pack(side="left", fill="x", expand=True, padx=5)
        
        ctk.CTkLabel(left_col, text="Input File:", font=ctk.CTkFont(size=12)).pack(anchor="w")
        self.aes_input_entry = ctk.CTkEntry(left_col, width=350)
        self.aes_input_entry.pack(pady=5)
        ctk.CTkButton(left_col, text="Browse", width=100,
                     command=lambda: self.browse_file(self.aes_input_entry)).pack()
        
        right_col = ctk.CTkFrame(io_frame)
        right_col.pack(side="left", fill="x", expand=True, padx=5)
        
        ctk.CTkLabel(right_col, text="Output File:", font=ctk.CTkFont(size=12)).pack(anchor="w")
        self.aes_output_entry = ctk.CTkEntry(right_col, width=350)
        self.aes_output_entry.pack(pady=5)
        ctk.CTkButton(right_col, text="Browse", width=100,
                     command=lambda: self.save_file(self.aes_output_entry)).pack()
        
        # Result area
        result_label = ctk.CTkLabel(main_frame, text="Result Preview:", 
                                   font=ctk.CTkFont(size=14))
        result_label.pack(pady=(10, 5))
        
        self.aes_result_text = ctk.CTkTextbox(main_frame, width=850, height=100)
        self.aes_result_text.pack(padx=20, pady=5)
        
        # Buttons
        btn_frame = ctk.CTkFrame(main_frame)
        btn_frame.pack(pady=15)
        
        ctk.CTkButton(btn_frame, text="🔐 Execute AES", width=200, height=40,
                     font=ctk.CTkFont(size=14, weight="bold"),
                     command=self.execute_aes).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Clear", width=100, height=40,
                     command=self.clear_aes).pack(side="left", padx=10)
    
    # Helper functions
    def browse_file(self, entry_widget):
        filename = filedialog.askopenfilename(
            title="Select file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            entry_widget.delete(0, "end")
            entry_widget.insert(0, filename)
    
    def save_file(self, entry_widget):
        filename = filedialog.asksaveasfilename(
            title="Save file",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            entry_widget.delete(0, "end")
            entry_widget.insert(0, filename)
    
    def generate_des_key(self):
        import secrets
        key = secrets.token_hex(8)
        self.des_key_entry.delete(0, "end")
        self.des_key_entry.insert(0, key)
    
    def generate_des_iv(self):
        import secrets
        iv = secrets.token_hex(8)
        self.des_iv_entry.delete(0, "end")
        self.des_iv_entry.insert(0, iv)
    
    def generate_aes_key(self):
        import secrets
        keysize = int(self.aes_keysize_var.get()) // 8
        key = secrets.token_hex(keysize)
        self.aes_key_entry.delete(0, "end")
        self.aes_key_entry.insert(0, key)
    
    def generate_aes_iv(self):
        import secrets
        iv = secrets.token_hex(16)
        self.aes_iv_entry.delete(0, "end")
        self.aes_iv_entry.insert(0, iv)
    
    # Placeholder functions for algorithm execution
    def crack_caesar(self):
        messagebox.showinfo("Info", "Caesar cipher cracking function - To be implemented")
    
    def crack_mono(self):
        messagebox.showinfo("Info", "Mono-alphabetic cracking function - To be implemented")
    
    def crack_vigenere(self):
        messagebox.showinfo("Info", "Vigenère cracking function - To be implemented")
    
    def execute_des(self):
        messagebox.showinfo("Info", "DES encryption/decryption function - To be implemented")
    
    def execute_aes(self):
        messagebox.showinfo("Info", "AES encryption/decryption function - To be implemented")
    
    # Clear functions
    def clear_caesar(self):
        self.caesar_input_entry.delete(0, "end")
        self.caesar_output_entry.delete(0, "end")
        self.caesar_result_text.delete("1.0", "end")
    
    def clear_mono(self):
        self.mono_input_entry.delete(0, "end")
        self.mono_output_entry.delete(0, "end")
        self.mono_result_text.delete("1.0", "end")
    
    def clear_vigenere(self):
        self.vigenere_input_entry.delete(0, "end")
        self.vigenere_output_entry.delete(0, "end")
        self.vigenere_result_text.delete("1.0", "end")
    
    def clear_des(self):
        self.des_input_entry.delete(0, "end")
        self.des_output_entry.delete(0, "end")
        self.des_key_entry.delete(0, "end")
        self.des_iv_entry.delete(0, "end")
        self.des_result_text.delete("1.0", "end")
    
    def clear_aes(self):
        self.aes_input_entry.delete(0, "end")
        self.aes_output_entry.delete(0, "end")
        self.aes_key_entry.delete(0, "end")
        self.aes_iv_entry.delete(0, "end")
        self.aes_result_text.delete("1.0", "end")

if __name__ == "__main__":
    app = CryptoApp()
    app.mainloop()