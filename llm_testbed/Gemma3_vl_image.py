"""
Gemma3 4B 4bit Quantized Vision Analysis
이 스크립트는 Gemma3 4B 모델의 4bit 양자화 버전을 사용하여 이미지와 비디오를 분석합니다.
"""

import torch
from transformers import AutoProcessor, Gemma3ForConditionalGeneration, BitsAndBytesConfig
from PIL import Image
import requests
import cv2
import numpy as np
from typing import List, Optional, Union
import os
import warnings
warnings.filterwarnings('ignore')


class Gemma3VisionAnalyzer:
    """Gemma3 4B 4bit 양자화 모델을 사용한 비전 분석기"""
    
    def __init__(self, use_qat=False):
        """
        초기화 메서드
        
        Args:
            use_qat (bool): QAT(Quantization-Aware Training) 모델 사용 여부
        """
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")
        
        # 모델 ID 설정
        if use_qat:
            # Google의 공식 QAT 양자화 모델 (메모리 효율성 극대화)
            self.model_id = "google/gemma-3-4b-it-qat"
            print("QAT(Quantization-Aware Training) 모델을 로드합니다...")
            self._load_qat_model()
        else:
            # 일반 모델 + BitsAndBytes 4bit 양자화
            self.model_id = "google/gemma-3-4b-it"
            print("BitsAndBytes 4bit 양자화를 사용하여 모델을 로드합니다...")
            self._load_quantized_model()
        
        print(f"모델 로드 완료: {self.model_id}")
        self.print_memory_usage()
    
    def _load_quantized_model(self):
        """BitsAndBytes를 사용한 4bit 양자화 모델 로드"""
        # 4bit 양자화 설정
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.bfloat16,  # 연산 시 사용할 데이터 타입
            bnb_4bit_quant_type="nf4",  # NF4 양자화 타입 사용
            bnb_4bit_use_double_quant=True  # 이중 양자화로 추가 메모리 절약
        )
        
        # 모델과 프로세서 로드
        self.model = Gemma3ForConditionalGeneration.from_pretrained(
            self.model_id,
            device_map="auto",
            quantization_config=quantization_config,
            torch_dtype=torch.bfloat16
        ).eval()
        
        self.processor = AutoProcessor.from_pretrained(self.model_id)
    
    def _load_qat_model(self):
        """Google의 QAT 양자화 모델 로드"""
        # QAT 모델은 이미 양자화되어 있어 별도 설정 불필요
        self.model = Gemma3ForConditionalGeneration.from_pretrained(
            self.model_id,
            device_map="auto",
            torch_dtype="auto"
        ).eval()
        
        self.processor = AutoProcessor.from_pretrained(self.model_id)
    
    def analyze_image(self, 
                     image_source: Union[str, Image.Image], 
                     prompt: str = "이 이미지를 자세히 설명해주세요.") -> str:
        """
        이미지를 분석하고 설명을 생성
        
        Args:
            image_source: 이미지 파일 경로, URL, 또는 PIL Image 객체
            prompt: 이미지와 함께 사용할 프롬프트
        
        Returns:
            생성된 텍스트 응답
        """
        # 이미지 로드
        image = self._load_image(image_source)
        
        # 메시지 포맷 설정
        messages = [
            {
                "role": "system",
                "content": [{"type": "text", "text": "당신은 이미지를 분석하는 도움이 되는 어시스턴트입니다."}]
            },
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": image},
                    {"type": "text", "text": prompt}
                ]
            }
        ]
        
        # 입력 처리
        inputs = self.processor.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt"
        ).to(self.model.device, dtype=torch.bfloat16)
        
        # 텍스트 생성 (Gemma 팀 권장 설정)
        with torch.inference_mode():
            generation = self.model.generate(
                **inputs,
                max_new_tokens=500,
                temperature=1.0,
                top_k=64,
                top_p=0.95,
                do_sample=True
            )
        
        # 생성된 토큰만 추출
        input_len = inputs["input_ids"].shape[-1]
        generated_tokens = generation[0][input_len:]
        
        # 디코딩
        response = self.processor.decode(generated_tokens, skip_special_tokens=True)
        
        return response
    
    def _load_image(self, image_source: Union[str, Image.Image]) -> Image.Image:
        """이미지 로드 헬퍼 함수"""
        if isinstance(image_source, str):
            if image_source.startswith(('http://', 'https://')):
                # URL인 경우
                image = Image.open(requests.get(image_source, stream=True).raw)
            else:
                # 파일 경로인 경우
                image = Image.open(image_source)
        elif isinstance(image_source, Image.Image):
            image = image_source
        else:
            raise ValueError("image_source는 파일 경로, URL, 또는 PIL Image 객체여야 합니다.")
        
        return image
    
    def analyze_multiple_images(self, 
                               image_sources: List[Union[str, Image.Image]], 
                               prompts: Optional[List[str]] = None) -> List[dict]:
        """
        여러 이미지를 배치로 분석
        
        Args:
            image_sources: 이미지 소스들의 리스트
            prompts: 각 이미지에 대한 프롬프트 리스트 (선택사항)
        
        Returns:
            분석 결과 리스트
        """
        if prompts is None:
            prompts = ["이 이미지를 설명해주세요."] * len(image_sources)
        
        results = []
        for idx, (image_source, prompt) in enumerate(zip(image_sources, prompts)):
            print(f"이미지 {idx + 1}/{len(image_sources)} 분석 중...")
            try:
                result = self.analyze_image(image_source, prompt)
                results.append({
                    "index": idx,
                    "image": image_source,
                    "prompt": prompt,
                    "response": result,
                    "status": "success"
                })
            except Exception as e:
                results.append({
                    "index": idx,
                    "image": image_source,
                    "prompt": prompt,
                    "error": str(e),
                    "status": "failed"
                })
        
        return results
    
    def analyze_video_frames(self,
                           video_path: str,
                           frame_interval: int = 30,
                           max_frames: Optional[int] = None,
                           prompt_template: str = "프레임 {frame_num}에서 무슨 일이 일어나고 있나요?") -> List[dict]:
        """
        비디오에서 프레임을 추출하여 분석
        
        Args:
            video_path: 비디오 파일 경로
            frame_interval: 분석할 프레임 간격
            max_frames: 최대 분석할 프레임 수
            prompt_template: 프레임 번호를 포함한 프롬프트 템플릿
        
        Returns:
            프레임 분석 결과 리스트
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"비디오 파일을 찾을 수 없습니다: {video_path}")
        
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        results = []
        frame_count = 0
        analyzed_count = 0
        
        print(f"비디오 분석 시작: {video_path}")
        print(f"FPS: {fps}, 프레임 간격: {frame_interval}")
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            if frame_count % frame_interval == 0:
                # OpenCV BGR을 RGB로 변환
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_image = Image.fromarray(rgb_frame)
                
                # 프레임 분석
                prompt = prompt_template.format(frame_num=frame_count)
                print(f"프레임 {frame_count} 분석 중...")
                
                try:
                    analysis = self.analyze_image(pil_image, prompt)
                    results.append({
                        "frame_number": frame_count,
                        "timestamp": frame_count / fps,
                        "analysis": analysis,
                        "status": "success"
                    })
                except Exception as e:
                    results.append({
                        "frame_number": frame_count,
                        "timestamp": frame_count / fps,
                        "error": str(e),
                        "status": "failed"
                    })
                
                analyzed_count += 1
                if max_frames and analyzed_count >= max_frames:
                    break
            
            frame_count += 1
        
        cap.release()
        print(f"비디오 분석 완료: {analyzed_count}개 프레임 분석됨")
        
        return results
    
    def print_memory_usage(self):
        """모델의 메모리 사용량 출력"""
        if torch.cuda.is_available():
            allocated = torch.cuda.memory_allocated() / 1024**3  # GB
            reserved = torch.cuda.memory_reserved() / 1024**3    # GB
            print(f"\nGPU 메모리 사용량:")
            print(f"  할당됨: {allocated:.2f} GB")
            print(f"  예약됨: {reserved:.2f} GB")
        else:
            print("GPU를 사용할 수 없습니다.")


def main():
    """메인 실행 함수"""
    print("=== Gemma3 4B 4bit Vision Analyzer ===\n")
    
    # 분석기 초기화 (QAT 모델 사용 옵션)
    # analyzer = Gemma3VisionAnalyzer(use_qat=True)  # QAT 모델 사용
    analyzer = Gemma3VisionAnalyzer(use_qat=False)  # BitsAndBytes 4bit 양자화 사용
    
    # 예시 1: 단일 이
