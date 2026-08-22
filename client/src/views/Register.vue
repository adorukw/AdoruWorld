<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { authApi } from "@/api";
import Layout from "@/components/layout/Layout.vue";
import PixelButton from "@/components/ui/PixelButton.vue";

const router = useRouter();

const step = ref<"form" | "verify">("form");
const username = ref("");
const email = ref("");
const password = ref("");
const code = ref("");
const errorMsg = ref("");
const infoMsg = ref("");
const submitting = ref(false);

async function handleRegister() {
    errorMsg.value = "";
    infoMsg.value = "";
    if (username.value.length < 3) {
        errorMsg.value = "用户名至少 3 个字符";
        return;
    }
    if (password.value.length < 8) {
        errorMsg.value = "密码至少 8 位";
        return;
    }
    submitting.value = true;
    try {
        const res = await authApi.register({
            username: username.value,
            email: email.value,
            password: password.value,
        });
        infoMsg.value = res.message;
        step.value = "verify";
    } catch (e: any) {
        errorMsg.value = e.message || "注册失败";
    } finally {
        submitting.value = false;
    }
}

async function handleVerify() {
    errorMsg.value = "";
    if (code.value.length !== 6) {
        errorMsg.value = "请输入 6 位验证码";
        return;
    }
    submitting.value = true;
    try {
        await authApi.verifyEmail({ email: email.value, code: code.value });
        router.push("/login");
    } catch (e: any) {
        errorMsg.value = e.message || "验证失败";
    } finally {
        submitting.value = false;
    }
}

async function handleResend() {
  errorMsg.value = "";
  try {
    await authApi.resendCode(email.value);
    infoMsg.value = "验证码已重新发送";
  } catch (e: any) {
    errorMsg.value = e.message || "发送失败";
  }
}
</script>

<template>
    <Layout>
        <section class="py-16">
            <div class="max-w-md mx-auto px-4">
                <div
                    class="bg-white border-4 border-black rounded-xl p-8 shadow-[8px_8px_0px_0px_rgba(0,0,0,1)]"
                >
                    <div class="text-center mb-8">
                        <div class="text-5xl mb-3">📝</div>
                        <h1 class="pixel-text text-2xl">注册</h1>
                        <p class="text-sm text-gray-500 mt-2">
                            注册后为访客角色，写权限由管理员分配
                        </p>
                    </div>

                    <!-- 第一步：填写信息 -->
                    <form v-if="step === 'form'" class="space-y-5" @submit.prevent="handleRegister">
                        <div>
                            <label class="block mb-2 pixel-text text-sm">用户名</label>
                            <input
                                v-model="username"
                                type="text"
                                placeholder="3-30 个字符"
                                class="w-full p-3 border-4 border-black focus:outline-none focus:ring-2 focus:ring-sky"
                            />
                        </div>
                        <div>
                            <label class="block mb-2 pixel-text text-sm">邮箱</label>
                            <input
                                v-model="email"
                                type="email"
                                placeholder="用于接收验证码"
                                class="w-full p-3 border-4 border-black focus:outline-none focus:ring-2 focus:ring-sky"
                            />
                        </div>
                        <div>
                            <label class="block mb-2 pixel-text text-sm">密码</label>
                            <input
                                v-model="password"
                                type="password"
                                placeholder="至少 8 位"
                                class="w-full p-3 border-4 border-black focus:outline-none focus:ring-2 focus:ring-sky"
                            />
                        </div>

                        <div v-if="errorMsg" class="text-red-500 pixel-text text-sm bg-red-50 border-2 border-red-300 p-3">
                            {{ errorMsg }}
                        </div>

                        <PixelButton
                            class="w-full !justify-center"
                            type="submit"
                            :loading="submitting"
                        >
                            <span class="w-full text-center">注册并获取验证码</span>
                        </PixelButton>
                    </form>

                    <!-- 第二步：输入验证码 -->
                    <form v-else class="space-y-5" @submit.prevent="handleVerify">
                        <div
                            class="text-sm bg-sky-50 border-2 border-sky-300 p-3"
                        >
                            {{ infoMsg || "验证码已发送至邮箱" }}
                            <span class="font-bold">{{ email }}</span>
                            <div class="text-xs text-gray-500 mt-1">
                                开发模式（console）下，验证码会打印在后端终端日志里
                            </div>
                        </div>
                        <div>
                            <label class="block mb-2 pixel-text text-sm">验证码</label>
                            <input
                                v-model="code"
                                type="text"
                                maxlength="6"
                                placeholder="6 位数字"
                                class="w-full p-3 border-4 border-black text-center text-2xl tracking-[0.5em] focus:outline-none focus:ring-2 focus:ring-sky"
                            />
                        </div>

                        <div v-if="errorMsg" class="text-red-500 pixel-text text-sm bg-red-50 border-2 border-red-300 p-3">
                            {{ errorMsg }}
                        </div>

                        <PixelButton
                            class="w-full !justify-center"
                            type="submit"
                            :loading="submitting"
                        >
                            <span class="w-full text-center">✅ 验证并完成注册</span>
                        </PixelButton>
                        <button
                            type="button"
                            class="w-full text-sm text-gray-500 hover:text-sky-700"
                            @click="handleResend"
                        >
                            没收到？60 秒后可重新发送
                        </button>
                    </form>

                    <div class="mt-6 text-center text-sm">
                        已有账号？
                        <router-link to="/login" class="text-sky-700 font-bold">
                            去登录
                        </router-link>
                    </div>
                </div>
            </div>
        </section>
    </Layout>
</template>
